from typing import NewType, Union, Literal


Language = NewType('Language', Union[
    Literal["af"],
    Literal["am"],
    Literal["ar"],
    Literal["bg"],
    Literal["bn"],
    Literal["bs"],
    Literal["ca"],
    Literal["cs"],
    Literal["cy"],
    Literal["da"],
    Literal["de"],
    Literal["el"],
    Literal["en"],
    Literal["es"],
    Literal["et"],
    Literal["eu"],
    Literal["fi"],
    Literal["fr"],
    Literal["gl"],
    Literal["gu"],
    Literal["ha"],
    Literal["hi"],
    Literal["hr"],
    Literal["hu"],
    Literal["id"],
    Literal["is"],
    Literal["it"],
    Literal["iw"],
    Literal["ja"],
    Literal["jw"],
    Literal["km"],
    Literal["kn"],
    Literal["ko"],
    Literal["la"],
    Literal["lt"],
    Literal["lv"],
    Literal["ml"],
    Literal["mr"],
    Literal["ms"],
    Literal["my"],
    Literal["ne"],
    Literal["nl"],
    Literal["no"],
    Literal["pa"],
    Literal["pl"],
    Literal["pt"],
    Literal["pt-]PT"],
    Literal["ro"],
    Literal["ru"],
    Literal["si"],
    Literal["sk"],
    Literal["sq"],
    Literal["sr"],
    Literal["su"],
    Literal["sv"],
    Literal["sw"],
    Literal["ta"],
    Literal["te"],
    Literal["th"],
    Literal["tl"],
    Literal["tr"],
    Literal["uk"],
    Literal["ur"],
    Literal["vi"],
    Literal["yue"],
    Literal["zh-CN"],
    Literal["zh-TW"] ]
)