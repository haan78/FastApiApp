from project import Project
from router import router

prj = Project(".env")
router(prj)

if __name__ == "__main__":
    prj.run()
