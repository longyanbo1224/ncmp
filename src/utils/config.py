import json
import os
import random
from typing import Dict, Any, Optional

class Config:
    def __init__(self):
        self.config_data: Dict = self._load_config()
    
    def _load_config(self) -> Dict:
        if self._check_env_variables():
            return self._load_from_env()
        return self._load_from_file()
    
    def _check_env_variables(self) -> bool:
        required_vars = ["MUSIC_U", "CSRF"]
        return all(os.getenv(var) for var in required_vars)
    
    def _load_from_env(self) -> Dict:
        config = {}
        
        # 必需的环境变量
        config["Cookie_MUSIC_U"] = os.getenv("MUSIC_U")
        config["Cookie___csrf"] = os.getenv("CSRF")
        
        # 可选的环境变量
        if notify_email := os.getenv("NOTIFY_EMAIL"):
            config["notify_email"] = notify_email
        if email_password := os.getenv("EMAIL_PASSWORD"):
            config["email_password"] = email_password
        if smtp_server := os.getenv("SMTP_SERVER"):
            config["smtp_server"] = smtp_server
        if smtp_port := os.getenv("SMTP_PORT"):
            config["smtp_port"] = int(smtp_port)
        if wait_min := os.getenv("WAIT_TIME_MIN"):
            config["wait_time_min"] = float(wait_min)
        if wait_max := os.getenv("WAIT_TIME_MAX"):
            config["wait_time_max"] = float(wait_max)
            
        config.setdefault("wait_time_min", 15)
        config.setdefault("wait_time_max", 20)
        
        return config
    
    def _load_from_file(self) -> Dict:
        try:
            config_path = "config/setting.json"
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"配置文件 {config_path} 不存在")
                
            with open(config_path, "r", encoding="utf-8") as file:
                config = json.loads(file.read())
                
            self._validate_config(config)
            return config
            
        except Exception as e:
            raise RuntimeError(f"配置加载失败: {str(e)}")
            
    def _validate_config(self, config: Dict) -> None:
        required_keys = ["Cookie_MUSIC_U", "Cookie___csrf"]
        for key in required_keys:
            if not config.get(key):
                raise ValueError(f"配置文件中缺少必要的配置项: {key}")
        
        # 设置默认值
        config.setdefault("wait_time_min", 15)
        config.setdefault("wait_time_max", 20)
        config.setdefault("smtp_server", "smtp.gmail.com")
        config.setdefault("smtp_port", 465)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config_data.get(key, default)

    def get_wait_time(self) -> float:
        """获取随机等待时间"""
        min_time = float(self.get("wait_time_min", 15))
        max_time = float(self.get("wait_time_max", 20))
        return random.uniform(min_time, max_time)