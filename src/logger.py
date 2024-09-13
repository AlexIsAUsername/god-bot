from enum import Enum

class LoggerConfig(Enum):
    NONE = 0
    DEBUG = 1
    INFO = 2
    ALL = 3

class Logger:
    def __init__(self, _conf: LoggerConfig):
        if _conf == None:
            raise Exception("Missing logger configuration")
        
        self._conf = _conf
        
    
    def get_conf(self):
        return self._conf
    
    def debug(self, *args) -> None:
        
        output = " ".join([str(s) for s in args])
        
        allowed_confs = [LoggerConfig.ALL, LoggerConfig.DEBUG]
        
        if self._conf not in allowed_confs:
            return
        
        self.out(output)
        
    
    def info(self, *args) -> None:
        
        output = " ".join([str(s) for s in args])
        
        allowed_confs = [LoggerConfig.ALL, LoggerConfig.INFO]
        
        if self._conf not in allowed_confs:
            return
        
        self.out(output)
        
        
    
    
    def log(self, *args) -> None:
        
        output = " ".join([str(s) for s in args])
        self.out(output)
    
    @staticmethod
    def out(s: str):
        print(s)