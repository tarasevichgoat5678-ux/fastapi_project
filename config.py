from pydantic_settings import BaseSettings, SettingsConfigDict

class Config_put(BaseSettings):
    PUT : str
    model_config = SettingsConfigDict(env_file='.env')

popa = Config_put()

