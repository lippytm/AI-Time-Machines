"""Example time machine implementations."""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uuid

from ai_time_machines.core.base import BaseTimeMachine
from ai_time_machines.core.interfaces import TimelineEvent, Message


class SimpleTimeMachine(BaseTimeMachine):
    """A simple time machine implementation."""
    
    def __init__(self, machine_id: str = None, machine_name: str = "SimpleTimeMachine"):
        super().__init__(machine_id, machine_name)
        self.time_travel_log: List[Dict[str, Any]] = []
        self.max_time_range = timedelta(days=365)  # 1 year max
        self.energy_level = 100.0
        self.energy_per_travel = 10.0
    
    async def _travel_to_time_impl(self, target_time: datetime) -> bool:
        """Implement time travel logic."""
        current_time = self._current_time
        time_diff = abs((target_time - current_time).total_seconds())
        
        # Check if we have enough energy
        required_energy = self.energy_per_travel * (time_diff / 3600)  # Energy based on hours
        
        if required_energy > self.energy_level:
            self._logger.warning(f"Insufficient energy for time travel. Required: {required_energy}, Available: {self.energy_level}")
            return False
        
        # Check if target time is within allowed range
        if abs(target_time - datetime.now()) > self.max_time_range:
            self._logger.warning(f"Target time {target_time} is outside allowed range")
            return False
        
        # Perform time travel
        self._logger.info(f"Traveling from {current_time} to {target_time}")
        
        # Consume energy
        self.energy_level -= required_energy
        
        # Update current time
        self._current_time = target_time
        
        # Log the travel
        travel_record = {
            "travel_id": str(uuid.uuid4()),
            "from_time": current_time.isoformat(),
            "to_time": target_time.isoformat(),
            "energy_consumed": required_energy,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        self.time_travel_log.append(travel_record)
        
        # Broadcast time travel event
        await self.broadcast_event(
            "time_travel_completed",
            {
                "machine_id": self.component_id,
                "travel_record": travel_record
            }
        )
        
        return True
    
    async def _get_timeline_events_impl(self, start_time: datetime, end_time: datetime) -> List[TimelineEvent]:
        """Get timeline events in the specified range."""
        events = []
        
        # Generate some sample events based on our travel log
        for travel in self.time_travel_log:
            travel_time = datetime.fromisoformat(travel["to_time"])
            if start_time <= travel_time <= end_time:
                event = TimelineEvent(
                    id=travel["travel_id"],
                    timestamp=travel_time,
                    event_type="time_travel",
                    data=travel,
                    source_component=self.component_id
                )
                events.append(event)
        
        return events
    
    async def recharge_energy(self, amount: float = None) -> float:
        """Recharge the time machine's energy."""
        if amount is None:
            amount = 100.0 - self.energy_level  # Full recharge
        
        self.energy_level = min(100.0, self.energy_level + amount)
        self._logger.info(f"Recharged energy by {amount}. Current level: {self.energy_level}")
        
        return self.energy_level
    
    async def get_status(self) -> Dict[str, Any]:
        """Get the current status of the time machine."""
        return {
            "machine_name": self.machine_name,
            "current_time": self._current_time.isoformat(),
            "energy_level": self.energy_level,
            "total_travels": len(self.time_travel_log),
            "max_time_range_days": self.max_time_range.days,
            "operational": self.energy_level > 0
        }


class AdvancedTimeMachine(BaseTimeMachine):
    """An advanced time machine with branching timeline support."""
    
    def __init__(self, machine_id: str = None, machine_name: str = "AdvancedTimeMachine"):
        super().__init__(machine_id, machine_name)
        self.timeline_branches: Dict[str, Dict[str, Any]] = {}
        self.current_branch = "main"
        self.branch_history: List[Dict[str, Any]] = []
        self.paradox_detection = True
        self.auto_resolve_paradoxes = True
    
    async def _on_initialize(self) -> None:
        """Initialize the advanced time machine."""
        await super()._on_initialize()
        
        # Create main timeline branch
        self.timeline_branches["main"] = {
            "created_at": datetime.now(),
            "branch_point": datetime.now(),
            "events": [],
            "active": True
        }
        
        # Register for timeline events
        self.register_event_handler("timeline_event", self._handle_timeline_event)
    
    async def _travel_to_time_impl(self, target_time: datetime) -> bool:
        """Advanced time travel with paradox detection."""
        current_time = self._current_time
        
        # Check for potential paradoxes
        if self.paradox_detection:
            paradox_risk = await self._detect_paradox_risk(target_time)
            if paradox_risk > 0.7:
                if self.auto_resolve_paradoxes:
                    branch_id = await self._create_paradox_branch(target_time)
                    self._logger.info(f"Created paradox resolution branch: {branch_id}")
                else:
                    self._logger.warning(f"High paradox risk detected for travel to {target_time}")
                    return False
        
        # Perform the time travel
        success = await super()._travel_to_time_impl(target_time)
        
        if success:
            # Record travel in current branch
            current_branch = self.timeline_branches[self.current_branch]
            current_branch["events"].append({
                "type": "time_travel",
                "from_time": current_time,
                "to_time": target_time,
                "timestamp": datetime.now(),
                "machine_id": self.component_id
            })
            
            # Check if we need to switch branches
            await self._update_branch_state(target_time)
        
        return success
    
    async def _create_timeline_branch_impl(self, branch_point: datetime, branch_id: str) -> bool:
        """Create a new timeline branch."""
        if branch_id in self.timeline_branches:
            self._logger.warning(f"Branch {branch_id} already exists")
            return False
        
        # Create the new branch
        self.timeline_branches[branch_id] = {
            "created_at": datetime.now(),
            "branch_point": branch_point,
            "parent_branch": self.current_branch,
            "events": [],
            "active": True
        }
        
        # Record branch creation
        self.branch_history.append({
            "action": "create_branch",
            "branch_id": branch_id,
            "branch_point": branch_point,
            "timestamp": datetime.now(),
            "created_by": self.component_id
        })
        
        self._logger.info(f"Created timeline branch '{branch_id}' at {branch_point}")
        
        # Broadcast branch creation event
        await self.broadcast_event(
            "timeline_branch_created",
            {
                "branch_id": branch_id,
                "branch_point": branch_point.isoformat(),
                "machine_id": self.component_id
            }
        )
        
        return True
    
    async def switch_to_branch(self, branch_id: str) -> bool:
        """Switch to a different timeline branch."""
        if branch_id not in self.timeline_branches:
            self._logger.error(f"Branch {branch_id} does not exist")
            return False
        
        if not self.timeline_branches[branch_id]["active"]:
            self._logger.error(f"Branch {branch_id} is not active")
            return False
        
        old_branch = self.current_branch
        self.current_branch = branch_id
        
        # Update current time to branch point if necessary
        branch_point = self.timeline_branches[branch_id]["branch_point"]
        if self._current_time != branch_point:
            self._current_time = branch_point
        
        self._logger.info(f"Switched from branch '{old_branch}' to '{branch_id}'")
        
        # Broadcast branch switch event
        await self.broadcast_event(
            "timeline_branch_switched",
            {
                "from_branch": old_branch,
                "to_branch": branch_id,
                "machine_id": self.component_id
            }
        )
        
        return True
    
    async def _detect_paradox_risk(self, target_time: datetime) -> float:
        """Detect the risk of creating a paradox."""
        # Simple paradox detection based on timeline density
        current_branch = self.timeline_branches[self.current_branch]
        events_near_target = 0
        
        for event in current_branch["events"]:
            event_time = event.get("to_time", event.get("timestamp"))
            if isinstance(event_time, str):
                event_time = datetime.fromisoformat(event_time)
            
            # Check if event is within 1 hour of target time
            if abs((event_time - target_time).total_seconds()) <= 3600:
                events_near_target += 1
        
        # Risk increases with event density
        risk = min(1.0, events_near_target / 10.0)
        return risk
    
    async def _create_paradox_branch(self, target_time: datetime) -> str:
        """Create a branch to resolve a potential paradox."""
        branch_id = f"paradox_resolution_{int(target_time.timestamp())}"
        await self._create_timeline_branch_impl(target_time, branch_id)
        await self.switch_to_branch(branch_id)
        return branch_id
    
    async def _update_branch_state(self, current_time: datetime) -> None:
        """Update the state of the current branch."""
        current_branch = self.timeline_branches[self.current_branch]
        
        # Update the latest time reached in this branch
        if "latest_time" not in current_branch or current_time > current_branch.get("latest_time", datetime.min):
            current_branch["latest_time"] = current_time
    
    async def _handle_timeline_event(self, message: Message) -> None:
        """Handle timeline events from other components."""
        payload = message.payload
        event_type = payload.get("event_type")
        event_data = payload.get("event_data", {})
        
        self._logger.debug(f"Received timeline event: {event_type}")
        
        # Add event to current branch
        current_branch = self.timeline_branches[self.current_branch]
        current_branch["events"].append({
            "type": "external_event",
            "event_type": event_type,
            "data": event_data,
            "timestamp": datetime.now(),
            "source": message.sender_id
        })
    
    async def get_branch_info(self, branch_id: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a timeline branch."""
        if branch_id is None:
            branch_id = self.current_branch
        
        if branch_id not in self.timeline_branches:
            return {}
        
        branch = self.timeline_branches[branch_id]
        return {
            "branch_id": branch_id,
            "created_at": branch["created_at"].isoformat(),
            "branch_point": branch["branch_point"].isoformat(),
            "parent_branch": branch.get("parent_branch"),
            "active": branch["active"],
            "event_count": len(branch["events"]),
            "latest_time": branch.get("latest_time", branch["branch_point"]).isoformat(),
            "is_current": branch_id == self.current_branch
        }
    
    async def list_branches(self) -> List[Dict[str, Any]]:
        """List all timeline branches."""
        branches = []
        for branch_id in self.timeline_branches:
            branch_info = await self.get_branch_info(branch_id)
            branches.append(branch_info)
        return branches
    
    async def merge_branches(self, source_branch: str, target_branch: str) -> bool:
        """Merge two timeline branches."""
        if source_branch not in self.timeline_branches or target_branch not in self.timeline_branches:
            self._logger.error(f"Cannot merge: one or both branches do not exist")
            return False
        
        source = self.timeline_branches[source_branch]
        target = self.timeline_branches[target_branch]
        
        # Merge events from source to target
        target["events"].extend(source["events"])
        target["events"].sort(key=lambda x: x.get("timestamp", datetime.min))
        
        # Deactivate source branch
        source["active"] = False
        
        # Record merge
        self.branch_history.append({
            "action": "merge_branches",
            "source_branch": source_branch,
            "target_branch": target_branch,
            "timestamp": datetime.now(),
            "merged_by": self.component_id
        })
        
        self._logger.info(f"Merged branch '{source_branch}' into '{target_branch}'")
        
        # If we were on the source branch, switch to target
        if self.current_branch == source_branch:
            await self.switch_to_branch(target_branch)
        
        return True