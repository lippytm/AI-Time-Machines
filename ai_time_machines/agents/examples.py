"""Example AI agent implementations."""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from ai_time_machines.core.base import BaseAgent
from ai_time_machines.core.interfaces import Message


class SimpleTaskAgent(BaseAgent):
    """A simple AI agent that processes basic tasks."""
    
    def __init__(self, agent_id: str = None, agent_name: str = "SimpleTaskAgent"):
        super().__init__(agent_id, agent_name)
        self.completed_tasks: List[Dict[str, Any]] = []
        self.task_count = 0
    
    async def _process_task_impl(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results."""
        task_type = task.get("type", "unknown")
        task_data = task.get("data", {})
        
        self._logger.info(f"Processing {task_type} task with data: {task_data}")
        
        # Simulate task processing
        await asyncio.sleep(0.1)
        
        result = {
            "task_id": task.get("id", f"task_{self.task_count}"),
            "status": "completed",
            "result": f"Processed {task_type} task successfully",
            "processed_at": datetime.now().isoformat(),
            "agent": self.agent_name
        }
        
        if task_type == "calculation":
            # Handle calculation tasks
            operation = task_data.get("operation", "add")
            numbers = task_data.get("numbers", [1, 2])
            
            if operation == "add":
                result["result"] = f"Sum of {numbers} = {sum(numbers)}"
            elif operation == "multiply":
                result["result"] = f"Product of {numbers} = {eval('*'.join(map(str, numbers)))}"
            else:
                result["result"] = f"Unknown operation: {operation}"
        
        elif task_type == "text_analysis":
            # Handle text analysis tasks
            text = task_data.get("text", "")
            word_count = len(text.split())
            char_count = len(text)
            result["result"] = f"Text analysis: {word_count} words, {char_count} characters"
        
        self.completed_tasks.append(result)
        self.task_count += 1
        
        return result
    
    async def _learn_from_feedback_impl(self, feedback: Dict[str, Any]) -> None:
        """Learn from feedback."""
        feedback_type = feedback.get("type", "unknown")
        self._logger.info(f"Received {feedback_type} feedback: {feedback.get('message', 'No message')}")
        
        # Simple learning: adjust behavior based on feedback
        if feedback_type == "positive":
            self._knowledge_base["positive_feedback_count"] = self._knowledge_base.get("positive_feedback_count", 0) + 1
        elif feedback_type == "negative":
            self._knowledge_base["negative_feedback_count"] = self._knowledge_base.get("negative_feedback_count", 0) + 1
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "agent_name": self.agent_name,
            "total_tasks": self.task_count,
            "completed_tasks": len(self.completed_tasks),
            "knowledge_base_size": len(self._knowledge_base),
            "positive_feedback": self._knowledge_base.get("positive_feedback_count", 0),
            "negative_feedback": self._knowledge_base.get("negative_feedback_count", 0)
        }


class CollaborativeAgent(BaseAgent):
    """An agent that can collaborate with other agents."""
    
    def __init__(self, agent_id: str = None, agent_name: str = "CollaborativeAgent"):
        super().__init__(agent_id, agent_name)
        self.collaboration_history: List[Dict[str, Any]] = []
        self.peer_agents: List[str] = []
    
    async def _on_initialize(self) -> None:
        """Initialize the collaborative agent."""
        await super()._on_initialize()
        
        # Register for collaboration events
        self.register_event_handler("collaboration_request", self._handle_collaboration_request)
        self.register_event_handler("collaboration_response", self._handle_collaboration_response)
    
    async def _process_task_impl(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task, potentially collaborating with other agents."""
        task_type = task.get("type", "unknown")
        complexity = task.get("complexity", "low")
        
        if complexity == "high" and task_type == "collaborative":
            # Request collaboration for complex tasks
            result = await self._collaborate_on_task(task)
        else:
            # Handle simple tasks independently
            result = await self._process_simple_task(task)
        
        return result
    
    async def _process_simple_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a simple task independently."""
        await asyncio.sleep(0.1)
        return {
            "task_id": task.get("id", "unknown"),
            "status": "completed",
            "result": f"Independently processed {task.get('type', 'unknown')} task",
            "processed_by": self.agent_name,
            "collaboration": False
        }
    
    async def _collaborate_on_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents on a complex task."""
        self._logger.info(f"Requesting collaboration for task: {task.get('id', 'unknown')}")
        
        # Find other collaborative agents
        from ai_time_machines.utils.registry import ComponentRegistry
        registry = await ComponentRegistry.get_instance()
        agents = await registry.list_components("agent")
        
        collaborators = [agent for agent in agents 
                        if agent.component_id != self.component_id 
                        and isinstance(agent, CollaborativeAgent)]
        
        if not collaborators:
            self._logger.warning("No collaborators available, processing independently")
            return await self._process_simple_task(task)
        
        # Send collaboration requests
        collaboration_id = f"collab_{task.get('id', 'unknown')}_{datetime.now().timestamp()}"
        responses = []
        
        for collaborator in collaborators[:2]:  # Limit to 2 collaborators
            await self.send_message(
                collaborator.component_id,
                "collaboration_request",
                {
                    "collaboration_id": collaboration_id,
                    "task": task,
                    "requester": self.component_id
                }
            )
        
        # Wait for responses (simplified - in reality would need timeout and error handling)
        await asyncio.sleep(0.5)
        
        # Combine results
        result = {
            "task_id": task.get("id", "unknown"),
            "status": "completed",
            "result": f"Collaboratively processed {task.get('type', 'unknown')} task",
            "processed_by": self.agent_name,
            "collaboration": True,
            "collaborators": [c.component_id for c in collaborators[:2]],
            "collaboration_id": collaboration_id
        }
        
        self.collaboration_history.append({
            "collaboration_id": collaboration_id,
            "task": task,
            "collaborators": [c.component_id for c in collaborators[:2]],
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    async def _handle_collaboration_request(self, message: Message) -> None:
        """Handle collaboration request from another agent."""
        payload = message.payload
        collaboration_id = payload.get("collaboration_id")
        task = payload.get("task")
        requester = payload.get("requester")
        
        self._logger.info(f"Received collaboration request {collaboration_id} from {requester}")
        
        # Process our part of the task
        our_contribution = f"Contribution from {self.agent_name} for {task.get('type', 'unknown')} task"
        
        # Send response
        await self.send_message(
            requester,
            "collaboration_response",
            {
                "collaboration_id": collaboration_id,
                "contribution": our_contribution,
                "status": "completed",
                "contributor": self.component_id
            }
        )
    
    async def _handle_collaboration_response(self, message: Message) -> None:
        """Handle collaboration response from another agent."""
        payload = message.payload
        collaboration_id = payload.get("collaboration_id")
        contribution = payload.get("contribution")
        contributor = payload.get("contributor")
        
        self._logger.info(f"Received collaboration response for {collaboration_id} from {contributor}")
        
        # Store the contribution (in a real system, this would be more sophisticated)
        for collab in self.collaboration_history:
            if collab["collaboration_id"] == collaboration_id:
                if "contributions" not in collab:
                    collab["contributions"] = []
                collab["contributions"].append({
                    "contributor": contributor,
                    "contribution": contribution
                })
                break


class LearningAgent(BaseAgent):
    """An agent that learns and adapts its behavior over time."""
    
    def __init__(self, agent_id: str = None, agent_name: str = "LearningAgent"):
        super().__init__(agent_id, agent_name)
        self.performance_history: List[Dict[str, Any]] = []
        self.learning_rate = 0.1
        self.adaptation_threshold = 5
    
    async def _process_task_impl(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task using learned knowledge."""
        task_type = task.get("type", "unknown")
        
        # Check if we have learned knowledge about this task type
        learned_behavior = self._knowledge_base.get(f"behavior_{task_type}")
        
        if learned_behavior:
            self._logger.info(f"Using learned behavior for {task_type} tasks")
            processing_time = learned_behavior.get("optimal_time", 0.1)
        else:
            self._logger.info(f"No learned behavior for {task_type}, using default")
            processing_time = 0.2
        
        # Simulate task processing with learned timing
        start_time = datetime.now()
        await asyncio.sleep(processing_time)
        end_time = datetime.now()
        
        actual_duration = (end_time - start_time).total_seconds()
        
        result = {
            "task_id": task.get("id", "unknown"),
            "status": "completed",
            "result": f"Processed {task_type} task using {'learned' if learned_behavior else 'default'} behavior",
            "processing_time": actual_duration,
            "used_learned_behavior": bool(learned_behavior),
            "agent": self.agent_name
        }
        
        # Record performance for learning
        self.performance_history.append({
            "task_type": task_type,
            "processing_time": actual_duration,
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
        # Trigger learning if we have enough data
        if len(self.performance_history) >= self.adaptation_threshold:
            await self._adapt_behavior()
        
        return result
    
    async def _learn_from_feedback_impl(self, feedback: Dict[str, Any]) -> None:
        """Learn from feedback and adjust behavior."""
        await super()._learn_from_feedback_impl(feedback)
        
        feedback_type = feedback.get("type")
        task_type = feedback.get("task_type")
        performance_rating = feedback.get("rating", 0.5)  # 0-1 scale
        
        if task_type and performance_rating is not None:
            # Update learning based on feedback
            behavior_key = f"behavior_{task_type}"
            current_behavior = self._knowledge_base.get(behavior_key, {"optimal_time": 0.2, "success_rate": 0.5})
            
            # Adjust optimal time based on performance rating
            if performance_rating > 0.7:
                # Good performance, try to be faster
                current_behavior["optimal_time"] *= (1 - self.learning_rate)
            elif performance_rating < 0.3:
                # Poor performance, slow down
                current_behavior["optimal_time"] *= (1 + self.learning_rate)
            
            # Update success rate
            current_behavior["success_rate"] = (
                current_behavior["success_rate"] * 0.9 + performance_rating * 0.1
            )
            
            self._knowledge_base[behavior_key] = current_behavior
            self._logger.info(f"Updated behavior for {task_type}: {current_behavior}")
    
    async def _adapt_behavior(self) -> None:
        """Adapt behavior based on performance history."""
        # Group performance by task type
        task_performance = {}
        
        for performance in self.performance_history[-self.adaptation_threshold:]:
            task_type = performance["task_type"]
            if task_type not in task_performance:
                task_performance[task_type] = []
            task_performance[task_type].append(performance["processing_time"])
        
        # Calculate optimal times for each task type
        for task_type, times in task_performance.items():
            if len(times) >= 3:  # Need enough data points
                avg_time = sum(times) / len(times)
                behavior_key = f"behavior_{task_type}"
                
                self._knowledge_base[behavior_key] = {
                    "optimal_time": avg_time * 0.9,  # Try to be 10% faster
                    "success_rate": 1.0,  # Assume success for now
                    "sample_size": len(times),
                    "last_updated": datetime.now().isoformat()
                }
                
                self._logger.info(f"Adapted behavior for {task_type}: optimal_time={avg_time * 0.9:.3f}s")
    
    async def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning and adaptation statistics."""
        base_stats = await self.get_statistics()
        
        learning_stats = {
            **base_stats,
            "learning_rate": self.learning_rate,
            "adaptation_threshold": self.adaptation_threshold,
            "performance_history_size": len(self.performance_history),
            "learned_behaviors": {k: v for k, v in self._knowledge_base.items() if k.startswith("behavior_")},
            "total_adaptations": len([k for k in self._knowledge_base.keys() if k.startswith("behavior_")])
        }
        
        return learning_stats