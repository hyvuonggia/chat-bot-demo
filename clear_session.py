import sqlite3
import sys
from app.core.config import settings

def clear_session(session_id: str):
    """Clear all checkpoints for a given session ID"""
    conn = sqlite3.connect(settings.sqlite_path)
    cursor = conn.cursor()
    
    # Count existing checkpoints
    cursor.execute("SELECT COUNT(*) FROM checkpoints WHERE thread_id = ?", (session_id,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"No checkpoints found for session: {session_id}")
    else:
        print(f"Found {count} checkpoints for session: {session_id}")
        
        # Delete checkpoints
        cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (session_id,))
        cursor.execute("DELETE FROM writes WHERE thread_id = ?", (session_id,))
        conn.commit()
        
        print(f"✅ Cleared all checkpoints for session: {session_id}")
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clear_session.py <session_id>")
        print("Example: python clear_session.py test-session-123")
        sys.exit(1)
    
    session_id = sys.argv[1]
    clear_session(session_id)
