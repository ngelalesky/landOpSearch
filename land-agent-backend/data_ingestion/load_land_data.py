import json
import random
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

class MockLandDataLoader:
    def __init__(self, num_samples: int = 1000):
        self.num_samples = num_samples
        
    def _generate_coordinates(self) -> List[float]:
        """Generate random coordinates within a reasonable range."""
        lat = random.uniform(37.0, 38.0)  # Example: San Francisco Bay Area
        lon = random.uniform(-122.5, -121.5)
        return [lon, lat]
    
    def _generate_polygon(self) -> Dict[str, Any]:
        """Generate a simple square polygon around a center point."""
        center = self._generate_coordinates()
        size = random.uniform(0.001, 0.01)  # Small area in degrees
        
        return {
            "type": "Polygon",
            "coordinates": [[
                [center[0] - size, center[1] - size],
                [center[0] + size, center[1] - size],
                [center[0] + size, center[1] + size],
                [center[0] - size, center[1] + size],
                [center[0] - size, center[1] - size]
            ]]
        }
    
    def _generate_land_features(self) -> Dict[str, Any]:
        """Generate mock land features."""
        return {
            "soil_type": random.choice(["clay", "sandy", "loamy", "silt"]),
            "elevation": random.uniform(0, 1000),
            "slope": random.uniform(0, 45),
            "water_access": random.choice([True, False]),
            "zoning": random.choice(["residential", "commercial", "agricultural", "mixed"]),
            "market_value": random.uniform(100000, 5000000),
            "last_sale_date": datetime.now().strftime("%Y-%m-%d"),
            "development_potential": random.uniform(0, 1)
        }
    
    def generate_geojson(self) -> Dict[str, Any]:
        """Generate a complete GeoJSON FeatureCollection."""
        features = []
        
        for _ in range(self.num_samples):
            feature = {
                "type": "Feature",
                "geometry": self._generate_polygon(),
                "properties": {
                    "id": f"LAND_{random.randint(1000, 9999)}",
                    **self._generate_land_features()
                }
            }
            features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    def save_to_file(self, filename: str = "mock_land_data.geojson"):
        """Save the generated data to a GeoJSON file."""
        data = self.generate_geojson()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename

if __name__ == "__main__":
    # Example usage
    loader = MockLandDataLoader(num_samples=100)
    output_file = loader.save_to_file()
    print(f"Generated mock land data saved to {output_file}") 