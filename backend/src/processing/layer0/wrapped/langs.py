from typing import List

from src.constants import DEFAULT_COLOR
from src.models import LangData, LangDatum, Language, UserPackage
from src.utils import format_number


def _count_loc(x: Language, metric: str) -> int:
    if metric == "changed":
        return x.additions + x.deletions
    return x.additions - x.deletions


def get_lang_data(data: UserPackage) -> LangData:
    out = {}
    for m in ["changed", "added"]:
        langs = sorted(
            data.contribs.total_stats.languages.items(),
            key=lambda x: _count_loc(x[1], m),
            reverse=True,
        )
        lang_objs: List[LangDatum] = []
        for k, v in list(langs)[:5]:
            lang_data = {
                "id": k,
                "label": k,
                "value": _count_loc(v, m),
                "formatted_value": format_number(_count_loc(v, m)),
                "color": v.color,
            }
            lang_objs.append(LangDatum.model_validate(lang_data))

        # remaining languages
        total_count = sum(_count_loc(v, m) for _, v in list(langs)[5:])
        lang_data = {
            "id": "other",
            "label": "other",
            "value": total_count,
            "formatted_value": format_number(total_count),
            "color": DEFAULT_COLOR,
        }
        if total_count > 100:
            lang_objs.append(LangDatum.model_validate(lang_data))

        out[f"langs_{m}"] = lang_objs

    return LangData.model_validate(out)
