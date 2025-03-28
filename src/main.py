import os
import subprocess
import ollama

# Clone the repository
def clone_repo(repo_url, local_path):
    if os.path.exists(local_path):
        print(f"Directory {local_path} already exists. Skipping cloning.")
        return
    subprocess.run(["git", "clone", repo_url, local_path])

# Split a large C file into logical sections
def split_c_file(c_code):
    # Split functions based on "{" or "}" for simplicity (use a more sophisticated parser in production)
    functions = c_code.split("}")  # This assumes functions end with "}"
    function_chunks = [f + "}" for f in functions if f.strip()]
    return function_chunks

# Translate C code chunk to Python
def translate_c_to_python(c_code_chunk):
    prompt = f"""
    You are an expert programmer skilled in both C and Python. Translate the following C code into Python:
    
    C Code:
    {c_code_chunk}
    
    Python Code:"""
    
    ollama_client = ollama.Client()
    response = ollama_client.generate(prompt=prompt, model="qwen2.5:0.5b")
    print(response)
    return response['response'].strip()  # Changed this line to access the response directly

# Process and translate large files
def process_large_c_file(c_file_path, output_dir):
    with open(c_file_path, 'r') as c_file:
        c_code = c_file.read()
    
    chunks = split_c_file(c_code)
    for idx, chunk in enumerate(chunks):
        print(f"Translating chunk {idx + 1}...")
        python_code = translate_c_to_python(chunk)
        python_file_path = os.path.join(output_dir, f"chunk_{idx + 1}.py")
        with open(python_file_path, 'w') as py_file:
            py_file.write(python_code)

# Process repository files
def process_repo(local_path):
    output_dir = os.path.join(local_path, "translated_files")
    os.makedirs(output_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if file.endswith(('.c', '.h')):
                c_file_path = os.path.join(root, file)
                print(f"Processing: {c_file_path}")
                process_large_c_file(c_file_path, output_dir)

# Main function
if __name__ == "__main__":
    repo_url = "https://github.com/callchain/lua-vm"  # Replace with your repo URL
    local_path = "./lua-vm"  # Local path to clone the repo
    clone_repo(repo_url, local_path)
    process_repo(local_path)