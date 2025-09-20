import os
import mlflow
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

from env_service.land_opportunity_env import LandOpportunityEnv

def create_env(land_data):
    """Create and wrap the environment."""
    env = LandOpportunityEnv(land_data)
    env = Monitor(env)
    return env

def train_ppo(
    land_data: dict,
    total_timesteps: int = 1_000_000,
    learning_rate: float = 3e-4,
    n_steps: int = 2048,
    batch_size: int = 64,
    n_epochs: int = 10,
    gamma: float = 0.99,
    gae_lambda: float = 0.95,
    clip_range: float = 0.2,
    ent_coef: float = 0.01,
    experiment_name: str = "land_opportunity_search"
):
    """Train a PPO agent on the land opportunity environment."""
    
    # Set up MLflow
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run():
        # Log hyperparameters
        mlflow.log_params({
            "learning_rate": learning_rate,
            "n_steps": n_steps,
            "batch_size": batch_size,
            "n_epochs": n_epochs,
            "gamma": gamma,
            "gae_lambda": gae_lambda,
            "clip_range": clip_range,
            "ent_coef": ent_coef
        })
        
        # Create and wrap environment
        env = create_env(land_data)
        env = DummyVecEnv([lambda: env])
        
        # Create evaluation environment
        eval_env = create_env(land_data)
        eval_env = DummyVecEnv([lambda: eval_env])
        
        # Create evaluation callback
        eval_callback = EvalCallback(
            eval_env,
            best_model_save_path="./best_model",
            log_path="./logs/",
            eval_freq=10000,
            deterministic=True,
            render=False
        )
        
        # Initialize PPO model
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            batch_size=batch_size,
            n_epochs=n_epochs,
            gamma=gamma,
            gae_lambda=gae_lambda,
            clip_range=clip_range,
            ent_coef=ent_coef,
            verbose=1
        )
        
        # Train the model
        model.learn(
            total_timesteps=total_timesteps,
            callback=eval_callback
        )
        
        # Save the final model
        model.save("final_model")
        mlflow.log_artifact("final_model.zip")
        
        # Log training metrics
        mlflow.log_metrics({
            "final_mean_reward": eval_callback.best_mean_reward
        })
        
        return model

if __name__ == "__main__":
    # Example usage
    from data_ingestion.load_land_data import MockLandDataLoader
    
    # Generate mock land data
    loader = MockLandDataLoader(num_samples=1000)
    land_data = loader.generate_geojson()
    
    # Train the agent
    model = train_ppo(land_data) 