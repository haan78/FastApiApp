from project import Project
from router import router

if __name__ == "__main__":
    prj = Project(".env")
    Project.run( router(prj),prj.port )
