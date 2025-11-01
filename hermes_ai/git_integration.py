"""
Hermes Config Generator - Git Integration
Version control for configuration files
"""

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class GitConfigManager:
    """Manages Git version control for Hermes configurations"""
    
    def __init__(self, repo_path: str = "./config_repo"):
        self.repo_path = Path(repo_path)
        self.repo_path.mkdir(parents=True, exist_ok=True)
        self._init_repo()
    
    def _init_repo(self):
        """Initialize Git repository if not exists"""
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            try:
                subprocess.run(
                    ["git", "init"],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
                # Create initial commit
                readme_path = self.repo_path / "README.md"
                readme_path.write_text("# Hermes Configuration Repository\n\nManaged by Hermes Config Generator\n")
                subprocess.run(
                    ["git", "add", "README.md"],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Git initialization failed: {e}")
    
    def save_config(self, config: Dict, feed_name: str, commit_message: Optional[str] = None) -> Dict:
        """
        Save configuration to Git repository
        
        Args:
            config: Configuration dictionary
            feed_name: Name of the feed
            commit_message: Optional commit message
        
        Returns:
            Result dictionary with commit info
        """
        try:
            # Create filename
            filename = f"{feed_name.lower().replace(' ', '_')}_config.json"
            file_path = self.repo_path / filename
            
            # Write config to file
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Git add
            subprocess.run(
                ["git", "add", filename],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            # Git commit
            if not commit_message:
                commit_message = f"Update configuration for {feed_name}"
            
            commit_message += f"\n\nGenerated: {datetime.now().isoformat()}"
            
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Get commit hash
            commit_hash = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()
            
            return {
                "success": True,
                "filename": filename,
                "commit_hash": commit_hash,
                "commit_message": commit_message,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e),
                "stderr": e.stderr.decode() if e.stderr else ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_history(self, feed_name: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get commit history for configurations
        
        Args:
            feed_name: Optional feed name to filter by
            limit: Maximum number of commits to return
        
        Returns:
            List of commit dictionaries
        """
        try:
            cmd = ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%an|%ae|%ad|%s"]
            
            if feed_name:
                filename = f"{feed_name.lower().replace(' ', '_')}_config.json"
                cmd.append(filename)
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commits.append({
                            "hash": parts[0],
                            "author": parts[1],
                            "email": parts[2],
                            "date": parts[3],
                            "message": parts[4]
                        })
            
            return commits
            
        except subprocess.CalledProcessError as e:
            return []
        except Exception as e:
            return []
    
    def get_config_version(self, feed_name: str, commit_hash: str) -> Optional[Dict]:
        """
        Get a specific version of a configuration
        
        Args:
            feed_name: Name of the feed
            commit_hash: Git commit hash
        
        Returns:
            Configuration dictionary or None
        """
        try:
            filename = f"{feed_name.lower().replace(' ', '_')}_config.json"
            
            result = subprocess.run(
                ["git", "show", f"{commit_hash}:{filename}"],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            return json.loads(result.stdout)
            
        except subprocess.CalledProcessError:
            return None
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
    
    def rollback(self, feed_name: str, commit_hash: str) -> Dict:
        """
        Rollback configuration to a previous version
        
        Args:
            feed_name: Name of the feed
            commit_hash: Git commit hash to rollback to
        
        Returns:
            Result dictionary
        """
        try:
            filename = f"{feed_name.lower().replace(' ', '_')}_config.json"
            
            # Get the old version
            old_config = self.get_config_version(feed_name, commit_hash)
            if not old_config:
                return {
                    "success": False,
                    "error": "Could not retrieve configuration from specified commit"
                }
            
            # Write it back
            file_path = self.repo_path / filename
            with open(file_path, 'w') as f:
                json.dump(old_config, f, indent=2)
            
            # Commit the rollback
            subprocess.run(
                ["git", "add", filename],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            commit_message = f"Rollback {feed_name} to {commit_hash[:7]}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            new_commit_hash = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()
            
            return {
                "success": True,
                "rolled_back_to": commit_hash,
                "new_commit": new_commit_hash,
                "message": f"Successfully rolled back to {commit_hash[:7]}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def diff(self, feed_name: str, commit1: str, commit2: str = "HEAD") -> Optional[str]:
        """
        Get diff between two versions of a configuration
        
        Args:
            feed_name: Name of the feed
            commit1: First commit hash
            commit2: Second commit hash (default: HEAD)
        
        Returns:
            Diff string or None
        """
        try:
            filename = f"{feed_name.lower().replace(' ', '_')}_config.json"
            
            result = subprocess.run(
                ["git", "diff", commit1, commit2, "--", filename],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            return result.stdout
            
        except subprocess.CalledProcessError:
            return None
        except Exception:
            return None
    
    def list_configs(self) -> List[str]:
        """
        List all configuration files in the repository
        
        Returns:
            List of configuration filenames
        """
        try:
            configs = []
            for file_path in self.repo_path.glob("*_config.json"):
                configs.append(file_path.name)
            return sorted(configs)
        except Exception:
            return []
    
    def get_config(self, feed_name: str) -> Optional[Dict]:
        """
        Get the current version of a configuration
        
        Args:
            feed_name: Name of the feed
        
        Returns:
            Configuration dictionary or None
        """
        try:
            filename = f"{feed_name.lower().replace(' ', '_')}_config.json"
            file_path = self.repo_path / filename
            
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
            
        except Exception:
            return None
    
    def compare_configs(self, feed_name1: str, feed_name2: str) -> Dict:
        """
        Compare two different configurations
        
        Args:
            feed_name1: First feed name
            feed_name2: Second feed name
        
        Returns:
            Comparison result dictionary
        """
        config1 = self.get_config(feed_name1)
        config2 = self.get_config(feed_name2)
        
        if not config1 or not config2:
            return {
                "success": False,
                "error": "One or both configurations not found"
            }
        
        differences = {}
        
        # Compare keys
        keys1 = set(config1.keys())
        keys2 = set(config2.keys())
        
        differences["only_in_first"] = list(keys1 - keys2)
        differences["only_in_second"] = list(keys2 - keys1)
        differences["common_keys"] = list(keys1 & keys2)
        
        # Compare common keys
        differences["different_values"] = []
        for key in differences["common_keys"]:
            if config1[key] != config2[key]:
                differences["different_values"].append({
                    "key": key,
                    "value_in_first": config1[key],
                    "value_in_second": config2[key]
                })
        
        return {
            "success": True,
            "feed1": feed_name1,
            "feed2": feed_name2,
            "differences": differences
        }


# Convenience function
def get_git_manager(repo_path: str = "./config_repo") -> GitConfigManager:
    """Get Git manager instance"""
    return GitConfigManager(repo_path)

# Alias for backward compatibility
GitIntegration = GitConfigManager
