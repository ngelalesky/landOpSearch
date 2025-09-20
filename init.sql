-- Initialize databases for Land Opportunity Search

-- Create main application database
CREATE DATABASE land_search;

-- Create MLflow database
CREATE DATABASE mlflow;

-- Create Airflow database
CREATE DATABASE airflow;

-- Create user for application
CREATE USER land_search_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE land_search TO land_search_user;
GRANT ALL PRIVILEGES ON DATABASE mlflow TO land_search_user;
GRANT ALL PRIVILEGES ON DATABASE airflow TO land_search_user;

-- Connect to land_search database and create schema
\c land_search;

-- Enable PostGIS extension for geospatial data
CREATE EXTENSION IF NOT EXISTS postgis;

-- Land parcels table
CREATE TABLE land_parcels (
    id SERIAL PRIMARY KEY,
    parcel_id VARCHAR(50) UNIQUE NOT NULL,
    coordinates GEOMETRY(POINT, 4326),
    soil_type VARCHAR(50),
    elevation DECIMAL(8,2),
    slope DECIMAL(5,2),
    water_access BOOLEAN,
    zoning VARCHAR(50),
    market_value DECIMAL(12,2),
    development_potential DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create spatial index
CREATE INDEX idx_land_parcels_coordinates ON land_parcels USING GIST (coordinates);

-- Satellite imagery metadata
CREATE TABLE satellite_imagery (
    id SERIAL PRIMARY KEY,
    parcel_id INTEGER REFERENCES land_parcels(id) ON DELETE CASCADE,
    image_url VARCHAR(500),
    capture_date DATE,
    cloud_cover DECIMAL(3,2),
    resolution VARCHAR(20),
    provider VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Model predictions
CREATE TABLE model_predictions (
    id SERIAL PRIMARY KEY,
    parcel_id INTEGER REFERENCES land_parcels(id) ON DELETE CASCADE,
    model_version VARCHAR(50),
    prediction_score DECIMAL(5,4),
    confidence DECIMAL(5,4),
    recommended_action INTEGER,
    features JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_model_predictions_parcel_id ON model_predictions(parcel_id);
CREATE INDEX idx_model_predictions_created_at ON model_predictions(created_at);
CREATE INDEX idx_model_predictions_score ON model_predictions(prediction_score);

-- API usage tracking
CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(100),
    method VARCHAR(10),
    response_time_ms INTEGER,
    status_code INTEGER,
    user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for API monitoring
CREATE INDEX idx_api_usage_endpoint ON api_usage(endpoint);
CREATE INDEX idx_api_usage_created_at ON api_usage(created_at);
CREATE INDEX idx_api_usage_status_code ON api_usage(status_code);

-- Grant permissions to application user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO land_search_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO land_search_user;

-- Connect to MLflow database
\c mlflow;

-- Grant permissions for MLflow
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO land_search_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO land_search_user;

-- Connect to Airflow database
\c airflow;

-- Grant permissions for Airflow
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO land_search_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO land_search_user;

-- Insert sample data for development
\c land_search;

-- Insert sample land parcels
INSERT INTO land_parcels (parcel_id, coordinates, soil_type, elevation, slope, water_access, zoning, market_value, development_potential) VALUES
('LAND_001', ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326), 'loamy', 50.0, 5.0, true, 'residential', 750000.00, 0.85),
('LAND_002', ST_SetSRID(ST_MakePoint(-122.4094, 37.7849), 4326), 'clay', 75.0, 8.0, false, 'commercial', 1200000.00, 0.92),
('LAND_003', ST_SetSRID(ST_MakePoint(-122.4294, 37.7649), 4326), 'sandy', 25.0, 2.0, true, 'mixed', 950000.00, 0.78);

-- Insert sample satellite imagery
INSERT INTO satellite_imagery (parcel_id, image_url, capture_date, cloud_cover, resolution, provider) VALUES
(1, 'https://example.com/satellite/land_001_2024.png', '2024-01-15', 0.05, '10m', 'sentinel'),
(2, 'https://example.com/satellite/land_002_2024.png', '2024-01-16', 0.12, '30m', 'landsat'),
(3, 'https://example.com/satellite/land_003_2024.png', '2024-01-17', 0.08, '10m', 'sentinel');

-- Insert sample predictions
INSERT INTO model_predictions (parcel_id, model_version, prediction_score, confidence, recommended_action, features) VALUES
(1, 'v1.0.0', 0.85, 0.92, 1, '{"x": 0.5, "y": 0.6, "soil_type": 0.8, "elevation": 0.3, "slope": 0.2, "water_access": 0.9, "zoning": 0.7, "market_value": 0.4, "development_potential": 0.6}'),
(2, 'v1.0.0', 0.92, 0.95, 2, '{"x": 0.4, "y": 0.7, "soil_type": 0.6, "elevation": 0.5, "slope": 0.4, "water_access": 0.2, "zoning": 0.9, "market_value": 0.8, "development_potential": 0.9}'),
(3, 'v1.0.0', 0.78, 0.88, 1, '{"x": 0.6, "y": 0.5, "soil_type": 0.7, "elevation": 0.2, "slope": 0.1, "water_access": 0.9, "zoning": 0.6, "market_value": 0.7, "development_potential": 0.5}');