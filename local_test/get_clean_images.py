from src.entities.v1.integrations.integrations import Integrations

if __name__ == "__main__":
    integrations = Integrations()
    status, message = integrations.clean_images()
    print(status, message)
