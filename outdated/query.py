from vectordb import Memory

memory = Memory(memory_file="memory.json")

query = "policy"
results = memory.search(query, top_n = 1)

print(results)