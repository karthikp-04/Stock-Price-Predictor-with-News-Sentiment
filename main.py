# main.py
import sys
import os

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Stock Market Predictor")
    print("=" * 50)
    print("\nOptions:")
    print("1. Run API server: python main.py api")
    print("2. Test predictor: python main.py test")
    print("3. Run demo: python main.py demo")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "api":
            print("\nStarting API server...")
            import uvicorn
            uvicorn.run("app.api.server:app", host="0.0.0.0", port=8000, reload=True)
            
        elif command == "test":
            print("\nTesting predictor...")
            from app.ml.predictor import test_predictor
            test_predictor()
            
        elif command == "demo":
            print("\nRunning demo...")
            from app.demo import run_demo
            run_demo()
    else:
        print("\nPlease specify a command.")