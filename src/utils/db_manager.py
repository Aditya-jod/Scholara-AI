import sqlite3
import json
import hashlib

DB_PATH = 'scholara.db'

def _get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    with _get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                source_text_hash TEXT NOT NULL,
                input_data_hash TEXT,
                output_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create an index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_cache
            ON agent_cache (agent_name, source_text_hash, input_data_hash)
        ''')
        conn.commit()
    print("[DB] Database initialized.")

def get_cached_result(agent_name, source_text, input_data=None):
    """
    Retrieves a cached result for a given agent and source text.
    
    Args:
        agent_name (str): The name of the agent (e.g., 'extractor', 'organizer').
        source_text (str): The raw source text.
        input_data (dict, optional): The input data for the agent, if any. Defaults to None.

    Returns:
        The cached output data if found, otherwise None.
    """
    source_hash = hashlib.sha256(source_text.encode()).hexdigest()
    input_hash = hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest() if input_data else None
    
    with _get_db_connection() as conn:
        cursor = conn.cursor()
        if input_hash:
            cursor.execute(
                "SELECT output_data FROM agent_cache WHERE agent_name = ? AND source_text_hash = ? AND input_data_hash = ?",
                (agent_name, source_hash, input_hash)
            )
        else:
            cursor.execute(
                "SELECT output_data FROM agent_cache WHERE agent_name = ? AND source_text_hash = ? AND input_data_hash IS NULL",
                (agent_name, source_hash)
            )
        row = cursor.fetchone()

    if row:
        print(f"[CACHE] Found cached result for agent '{agent_name}'.")
        return json.loads(row['output_data'])
    
    print(f"[CACHE] No cache found for agent '{agent_name}'.")
    return None

def set_cached_result(agent_name, source_text, output_data, input_data=None):
    """
    Caches the output of an agent.

    Args:
        agent_name (str): The name of the agent.
        source_text (str): The raw source text.
        output_data (any): The data to be cached (must be JSON serializable).
        input_data (dict, optional): The input data for the agent, if any. Defaults to None.
    """
    source_hash = hashlib.sha256(source_text.encode()).hexdigest()
    input_hash = hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest() if input_data else None
    
    with _get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO agent_cache (agent_name, source_text_hash, input_data_hash, output_data) VALUES (?, ?, ?, ?)",
            (agent_name, source_hash, input_hash, json.dumps(output_data))
        )
        conn.commit()
    print(f"[CACHE] Saved result for agent '{agent_name}'.")

if __name__ == '__main__':
    print("Running DB Manager self-test...")
    init_db()

    # Mock data
    mock_text = "This is a test."
    mock_input = {"key": "value"}
    mock_output = {"result": "This is the output."}

    # Test setting cache
    set_cached_result('test_agent', mock_text, mock_output, mock_input)

    # Test getting cache
    retrieved_output = get_cached_result('test_agent', mock_text, mock_input)
    assert retrieved_output == mock_output
    print("Cache hit test successful.")

    # Test cache miss
    retrieved_output_miss = get_cached_result('test_agent', "different text", mock_input)
    assert retrieved_output_miss is None
    print("Cache miss test successful.")

    print("DB Manager self-test complete.")
