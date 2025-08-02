from app.models import Base, engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done!")
