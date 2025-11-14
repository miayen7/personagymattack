"""
Controller module for PersonaGym-R Green Agent

Handles state management and reset functionality for assessment isolation
following AgentBeats requirements.
"""
import asyncio
import logging
from typing import Optional
from pathlib import Path
import shutil

class GreenAgentController:
    """
    Controls the green agent lifecycle and ensures assessment isolation.
    
    The controller is responsible for:
    - Resetting agent state between assessments
    - Managing temporary files and caches
    - Ensuring reproducible evaluation runs
    """
    
    def __init__(self, reports_dir: str = "reports", cache_dir: str = ".cache"):
        self.reports_dir = Path(reports_dir)
        self.cache_dir = Path(cache_dir)
        self.logger = logging.getLogger("GreenAgentController")
        self.current_assessment_id: Optional[str] = None
        
    async def reset(self) -> bool:
        """
        Reset the green agent state for a new assessment.
        
        This ensures assessment isolation by:
        1. Clearing temporary state
        2. Resetting counters
        3. Clearing caches (optional)
        
        Returns:
            bool: True if reset successful, False otherwise
        """
        try:
            self.logger.info("Resetting green agent state...")
            
            # Clear current assessment tracking
            self.current_assessment_id = None
            
            # Clear cache if it exists (optional - may want to preserve some data)
            if self.cache_dir.exists():
                self.logger.debug(f"Clearing cache directory: {self.cache_dir}")
                # Only clear temp files, not the entire cache
                for item in self.cache_dir.glob("temp_*"):
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            
            self.logger.info("Green agent reset completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during reset: {e}")
            return False
    
    async def prepare_assessment(self, assessment_id: str) -> bool:
        """
        Prepare for a new assessment.
        
        Args:
            assessment_id: Unique identifier for this assessment
            
        Returns:
            bool: True if preparation successful
        """
        try:
            self.logger.info(f"Preparing for assessment: {assessment_id}")
            
            # Reset first
            await self.reset()
            
            # Set new assessment ID
            self.current_assessment_id = assessment_id
            
            # Ensure reports directory exists
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Create assessment-specific directory
            assessment_dir = self.reports_dir / assessment_id
            assessment_dir.mkdir(exist_ok=True)
            
            self.logger.info(f"Assessment {assessment_id} ready")
            return True
            
        except Exception as e:
            self.logger.error(f"Error preparing assessment: {e}")
            return False
    
    async def cleanup_assessment(self, assessment_id: str) -> bool:
        """
        Clean up after an assessment completes.
        
        Args:
            assessment_id: Assessment to clean up
            
        Returns:
            bool: True if cleanup successful
        """
        try:
            self.logger.info(f"Cleaning up assessment: {assessment_id}")
            
            # Archive or compress results if needed
            # For now, just mark as complete
            
            if self.current_assessment_id == assessment_id:
                self.current_assessment_id = None
            
            self.logger.info(f"Assessment {assessment_id} cleaned up")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cleaning up assessment: {e}")
            return False
    
    def get_current_assessment(self) -> Optional[str]:
        """Get the ID of the currently running assessment."""
        return self.current_assessment_id
    
    async def health_check(self) -> dict:
        """
        Check controller health status.
        
        Returns:
            dict: Health status information
        """
        return {
            "controller_status": "healthy",
            "current_assessment": self.current_assessment_id,
            "reports_dir_exists": self.reports_dir.exists(),
            "cache_dir_exists": self.cache_dir.exists()
        }


class WhiteAgentResetClient:
    """
    Client for resetting white agents via their controller endpoints.
    
    White agents may also need reset between assessments. This client
    handles communication with white agent controllers.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("WhiteAgentResetClient")
    
    async def reset_white_agent(self, agent_url: str) -> bool:
        """
        Request a white agent to reset its state.
        
        Args:
            agent_url: Base URL of the white agent
            
        Returns:
            bool: True if reset successful
        """
        try:
            import httpx
            
            # Try standard A2A reset endpoint
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{agent_url}/a2a/reset")
                
                if response.status_code == 200:
                    self.logger.info(f"Successfully reset white agent: {agent_url}")
                    return True
                else:
                    self.logger.warning(
                        f"White agent reset returned status {response.status_code}"
                    )
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error resetting white agent {agent_url}: {e}")
            return False
    
    async def reset_multiple(self, agent_urls: list) -> dict:
        """
        Reset multiple white agents in parallel.
        
        Args:
            agent_urls: List of agent URLs to reset
            
        Returns:
            dict: Mapping of agent URL to reset success status
        """
        results = {}
        
        tasks = [
            self.reset_white_agent(url)
            for url in agent_urls
        ]
        
        reset_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for url, result in zip(agent_urls, reset_results):
            if isinstance(result, Exception):
                results[url] = False
                self.logger.error(f"Exception resetting {url}: {result}")
            else:
                results[url] = result
        
        return results
