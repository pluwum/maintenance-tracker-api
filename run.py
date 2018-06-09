from app import create_app
from instance.config import DevelopmentConfig

app = create_app()

app.config.from_object(DevelopmentConfig)

app.run()
