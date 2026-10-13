from app.model import train_and_save

if __name__ == "__main__":
    model = train_and_save()
    print(f"Trained demo model: {model.__class__.__name__}")
