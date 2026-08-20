from src.ai_agent.batch_processor import process_batch


IMAGE_PATHS = [
    "input/product3.jpeg"
]


results = process_batch(IMAGE_PATHS)


print("\n" + "=" * 70)
print("BATCH SUMMARY")
print("=" * 70)

for result in results:
    print(f"\nImage: {result.image_path}")
    print(f"Status: {result.status}")

    if result.draft_path:
        print(f"Draft: {result.draft_path}")

    if result.error:
        print(f"Error: {result.error}")
