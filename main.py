import re
import json as json_mod
from urllib.parse import quote

import aiohttp

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Image

PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.async_api import async_playwright

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass

WEATHER_API_MATCHING = "https://wis.qq.com/city/matching"
WEATHER_PAGE = "https://tianqi.qq.com/"
WEATHER_PAGE_SOURCE = "view-source:https://tianqi.qq.com/"
BLOCKED_DOMAINS = ["trace.qq.com"]


def parse_area_search(search: str) -> dict:
    cleaned = re.sub(r"\s+", " ", search).strip()
    reg = r"((.*)省)?((.*)市)?((.*)区)?"
    match = re.match(reg, cleaned)
    return {
        "province": match.group(2) or "",
        "city": match.group(4) or "",
        "district": match.group(6) or "",
        "raw": cleaned,
    }


async def resolve_area_id(search: str) -> dict | None:
    parsed = parse_area_search(search)
    province, city, district, raw = (
        parsed["province"],
        parsed["city"],
        parsed["district"],
        parsed["raw"],
    )

    candidates = [c for c in raw.split(" ") if c]
    candidates.reverse()
    candidates.append(raw.replace(" ", ""))

    area_id = -1
    internal_data = None

    async with aiohttp.ClientSession() as session:
        for candidate in candidates:
            url = f"{WEATHER_API_MATCHING}?source=xw&city={quote(candidate)}"
            try:
                async with session.get(url) as resp:
                    res = await resp.json()
            except Exception:
                continue

            if not isinstance(res, dict) or res.get("status") != 200:
                continue

            data = res.get("data")
            if not isinstance(data, dict):
                continue

            internal = data.get("internal")
            if not isinstance(internal, dict) or len(internal) == 0:
                continue
            keys = list(internal.keys())
            keys.reverse()

            for key in keys:
                name = internal[key]
                start_idx = candidates.index(candidate) + 1
                for j in range(start_idx, len(candidates)):
                    if name.find(candidates[j]) != -1 or candidates[j].find(name) != -1:
                        area_id = key
                        internal_data = internal
                        break
                if area_id != -1:
                    break
            if area_id != -1:
                break

    if area_id == -1:
        return None

    keys = list(internal_data.keys())
    keys.reverse()
    final_province = province
    final_city = city
    final_district = district

    for key in keys:
        parts = internal_data[key].split(", ")
        p = parts[0] if len(parts) > 0 else ""
        c = parts[1] if len(parts) > 1 else ""
        d = parts[2] if len(parts) > 2 else ""

        if province and province not in p:
            continue
        if city and city not in c:
            continue
        if district and district not in d:
            continue

        if p:
            final_province = p
        if c:
            final_city = c
        if d:
            final_district = d
        area_id = key
        break

    return {
        "area_id": area_id,
        "province": final_province,
        "city": final_city,
        "district": final_district,
    }


async def capture_weather_screenshot(area_info: dict) -> bytes:
    attention_city = json_mod.dumps(
        [
            {
                "province": area_info["province"],
                "city": area_info["city"],
                "district": area_info["district"],
                "isDefault": True,
            }
        ],
        ensure_ascii=False,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.set_viewport_size({"width": 1280, "height": 1320})

            await page.goto(WEATHER_PAGE_SOURCE)
            await page.evaluate(
                "(city) => { localStorage.setItem('attentionCity', city); }",
                attention_city,
            )

            async def handle_route(route):
                if any(d in route.request.url for d in BLOCKED_DOMAINS):
                    await route.abort()
                else:
                    await route.continue_()

            await page.route("**/*", handle_route)

            await page.goto(WEATHER_PAGE, wait_until="networkidle")

            await page.evaluate(
                """() => {
                document.querySelectorAll('a').forEach(function(el) { el.remove(); });
                var footer = document.getElementById('ct-footer');
                if (footer) footer.remove();
            }"""
            )

            await page.evaluate(
                """() => {
                var p = document.createElement('p');
                p.style.cssText = 'text-align: center; font-size: 15px; margin-top: -25px;';
                p.textContent = 'Created By AstrBot & astrbot_plugin_qq_weather';
                document.body.appendChild(p);
            }"""
            )

            body = await page.query_selector("body")
            img = await body.screenshot(type="jpeg", quality=100, omit_background=False)
            return img
        finally:
            await page.close()
            await browser.close()


_PLAYWRIGHT_INSTALL_MSG = (
    "❌ 未检测到 Playwright 依赖！请执行以下命令安装：\n"
    "pip install playwright\n"
    "playwright install chromium"
)
_PLAYWRIGHT_BROWSER_MSG = (
    "❌ 未检测到 Chromium 浏览器！请执行以下命令安装：\n"
    "playwright install chromium"
)


def _report_playwright_status():
    if not PLAYWRIGHT_AVAILABLE:
        logger.warning("[QQ天气] Playwright 未安装，请执行: pip install playwright && playwright install chromium")
    elif not PLAYWRIGHT_BROWSER_READY:
        logger.warning("[QQ天气] Chromium 浏览器未安装，请执行: playwright install chromium")
    else:
        logger.info("[QQ天气] Playwright + Chromium 依赖检测通过")


def _check_playwright_browser():
    import subprocess
    import sys

    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--dry-run", "chromium"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if "is already installed" in result.stdout or "is already installed" in result.stderr:
            return True
        if result.returncode != 0:
            return False
        return True
    except Exception:
        return False


PLAYWRIGHT_BROWSER_READY = PLAYWRIGHT_AVAILABLE and _check_playwright_browser()


@register("astrbot_plugin_qq_weather", "VanillaNahida", "QQ天气查询插件，使用腾讯天气接口截图", "1.0.0")
class QQWeatherPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        _report_playwright_status()

    @filter.command("天气")
    async def handle_weather(self, event: AstrMessageEvent, city: str):
        """天气查询，命令格式：/天气 <城市名>"""
        if not PLAYWRIGHT_AVAILABLE:
            yield event.plain_result(_PLAYWRIGHT_INSTALL_MSG)
            return
        if not PLAYWRIGHT_BROWSER_READY:
            yield event.plain_result(_PLAYWRIGHT_BROWSER_MSG)
            return

        city = city.strip()

        if not city:
            yield event.plain_result("查询格式：/天气 城市名\n例如：/天气 广州")
            return

        area_info = await resolve_area_id(city)
        if not area_info:
            yield event.plain_result("没有查询到该地区的天气！请检查您的输入，不要包含多余的信息，建议仅包含城市名/区名/县名。\n查询格式参考：/天气 广州")
            return

        try:
            img_buffer = await capture_weather_screenshot(area_info)
        except Exception as e:
            logger.error(f"[QQ天气] 截图异常: {e}")
            yield event.plain_result("天气截图失败！请查看控制台输出日志。")
            return

        if not img_buffer:
            yield event.plain_result("天气截图失败！请查看控制台输出日志。")
            return

        yield event.chain_result([Image.fromBytes(img_buffer)])
