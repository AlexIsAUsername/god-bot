from typing import TypedDict, NewType, Union, Literal
from gtts import lang
import json

from language import Language


FilePath = NewType('FilePath', str)


class Config(TypedDict):
    tts_language: Language  # type: ignore
    chain_order: int
    debug_mode: bool
    source_text: FilePath
    


def get_default_config():
    
    def_conf: Config = {
        'tts_language': "en",
        'chain_order': 4,
        'debug_mode': True,
        'source_text': "input/kjvc.txt"
    }
    
    return def_conf



def load_config(path: FilePath):
    if path == None:
        return get_default_config()
    
    raw_json = ""
    
    with open(path, "r") as f:
        raw_json = f.read()
        
    
    conf: Config = json.loads(raw_json)
    
    return conf
