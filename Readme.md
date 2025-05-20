### How to install the application 
1. Install uv package manager - [Reference Link](https://docs.astral.sh/uv/getting-started/installation/)
    
    On Mac:
    ```sh
    brew install uv
    ```
2. Start and activate virtual env using uv - [Reference Link](https://fastapi.tiangolo.com/virtual-environments/#create-a-virtual-environment)
    ```sh
    uv venv
    source .venv/bin/activate
    ```
3. Install dependencies
    ```sh
    uv pip install -r requirements.txt
    ```
4. Run the application
    ```
    uvicorn main:app --reload
    ```

