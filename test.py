import sys

try:
    import psycopg2
    print("Success! psycopg2 is found.")
except ImportError:
    print("Still not working.")
    
for path in sys.path:
    print(path)