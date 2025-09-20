import os
import random
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image
import requests
from datetime import datetime, timedelta

class MockSatelliteImageFetcher:
    def __init__(self, output_dir: str = "satellite_images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Mock satellite image providers
        self.providers = {
            "landsat": "https://landsat.gsfc.nasa.gov/wp-content/uploads/2021/08/landsat-9-1.jpg",
            "sentinel": "https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/resolutions/spatial",
            "planet": "https://www.planet.com/press-release/planet-launches-first-fully-integrated-satellite-imaging-system/"
        }
    
    def _generate_image_metadata(self, coordinates: Tuple[float, float]) -> Dict:
        """Generate mock metadata for a satellite image."""
        return {
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "provider": random.choice(list(self.providers.keys())),
            "resolution": random.choice(["10m", "30m", "60m"]),
            "bands": ["red", "green", "blue", "nir"],
            "cloud_cover": random.uniform(0, 0.3),
            "coordinates": coordinates
        }
    
    def _generate_mock_image(self, size: Tuple[int, int] = (256, 256)) -> np.ndarray:
        """Generate a mock satellite image."""
        # Create a random RGB image
        image = np.random.randint(0, 255, size=(*size, 3), dtype=np.uint8)
        
        # Add some structure to make it look more like a satellite image
        # Add some "roads" or "buildings"
        for _ in range(5):
            x = random.randint(0, size[0]-1)
            y = random.randint(0, size[1]-1)
            length = random.randint(10, 50)
            direction = random.choice(['horizontal', 'vertical'])
            
            if direction == 'horizontal':
                image[y, x:x+length] = [100, 100, 100]  # Gray for roads
            else:
                image[y:y+length, x] = [100, 100, 100]
        
        return image
    
    def fetch_image(self, coordinates: Tuple[float, float], 
                   image_id: str = None) -> Dict:
        """Fetch a mock satellite image for given coordinates."""
        if image_id is None:
            image_id = f"sat_{random.randint(1000, 9999)}"
        
        # Generate mock image
        image = self._generate_mock_image()
        
        # Save image
        image_path = os.path.join(self.output_dir, f"{image_id}.png")
        Image.fromarray(image).save(image_path)
        
        # Generate and return metadata
        metadata = self._generate_image_metadata(coordinates)
        metadata.update({
            "image_id": image_id,
            "image_path": image_path
        })
        
        return metadata
    
    def fetch_images_batch(self, coordinates_list: List[Tuple[float, float]]) -> List[Dict]:
        """Fetch multiple satellite images for a list of coordinates."""
        return [self.fetch_image(coords) for coords in coordinates_list]

if __name__ == "__main__":
    # Example usage
    fetcher = MockSatelliteImageFetcher()
    
    # Generate some random coordinates
    test_coordinates = [
        (37.7749, -122.4194),  # San Francisco
        (37.3382, -121.8863),  # San Jose
        (37.8715, -122.2730)   # Berkeley
    ]
    
    # Fetch images
    results = fetcher.fetch_images_batch(test_coordinates)
    
    # Print results
    for result in results:
        print(f"Fetched image {result['image_id']} from {result['provider']}")
        print(f"Saved to: {result['image_path']}")
        print(f"Cloud cover: {result['cloud_cover']:.2%}")
        print("---") 