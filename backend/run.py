import sys
import uvicorn
from router import Router

if __name__ == '__main__':
    reload = False
    port = 8001
    mode = "production"

    if len(sys.argv) > 1:        
        mode = str(sys.argv[1]).strip()   
        
    
    if len(sys.argv) > 2:
        port=int(sys.argv[2])

    print("Port = {}, Mode = {}".format(port,mode))

    reload = True if mode == "development" else False
    r = Router()
        
    uvicorn.run(r, host="0.0.0.0", port=8001, log_level="info", lifespan="off", reload=reload, port=port )