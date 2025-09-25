"""
🚀 MINIMAL, SAFE KNOWLEDGE SHARING SYSTEM
========================================
Ultra-safe knowledge sharing with independence monitoring safeguard
Only shares non-decision-influencing information to preserve algorithm independence
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import defaultdict, deque

# Configure logger
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MarketRegime(Enum):
    """Market regime classification"""
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"
    UNKNOWN = "unknown"


@dataclass
class RiskWarning:
    """Risk warning data structure"""
    symbol: str
    risk_type: str
    risk_level: RiskLevel
    timestamp: datetime
    description: str
    confidence: float
    data: Dict[str, Any]


@dataclass
class MarketRegimeInfo:
    """Market regime information"""
    symbol: str
    regime: MarketRegime
    confidence: float
    timestamp: datetime
    indicators: Dict[str, float]
    description: str


@dataclass
class DataQualityAlert:
    """Data quality alert"""
    symbol: str
    alert_type: str
    severity: str
    timestamp: datetime
    description: str
    affected_data: List[str]
    resolution_status: str


class IndependenceMonitor:
    """
    🛡️ INDEPENDENCE MONITOR SAFEGUARD
    =================================
    Monitors algorithm independence to prevent convergence
    Provides alerts when independence is at risk
    """
    
    def __init__(self, 
                 correlation_threshold: float = 0.6,
                 similarity_threshold: float = 0.7,
                 monitoring_window: int = 100):
        """
        Initialize independence monitor
        
        Args:
            correlation_threshold: Alert threshold for algorithm correlation
            similarity_threshold: Alert threshold for decision similarity
            monitoring_window: Number of decisions to monitor
        """
        self.correlation_threshold = correlation_threshold
        self.similarity_threshold = similarity_threshold
        self.monitoring_window = monitoring_window
        
        # Monitoring data
        self.algorithm_decisions = defaultdict(lambda: deque(maxlen=monitoring_window))
        self.correlation_history = deque(maxlen=1000)
        self.similarity_history = deque(maxlen=1000)
        self.independence_alerts = []
        
        # Independence metrics
        self.current_correlation = 0.0
        self.current_similarity = 0.0
        self.independence_score = 1.0
        
        logger.info("🛡️ Independence Monitor initialized", operation="enhanced_logging")
        logger.info(f"   📊 Correlation threshold: {correlation_threshold}", operation="enhanced_logging")
        logger.info(f"   📊 Similarity threshold: {similarity_threshold}", operation="enhanced_logging")
    
    def record_algorithm_decision(self, algorithm_id: str, decision: Dict[str, Any]):
        """Record algorithm decision for independence monitoring"""
        self.algorithm_decisions[algorithm_id].append({
            "timestamp": datetime.now(),
            "decision": decision,
            "confidence": decision.get("confidence", 0.0),
            "action": decision.get("action", "unknown")
        })
        
        # Update independence metrics
        self._update_independence_metrics()
    
    def _update_independence_metrics(self):
        """Update independence metrics based on recent decisions"""
        if len(self.algorithm_decisions) < 2:
            return
        
        # Calculate correlation between algorithms
        correlation = self._calculate_algorithm_correlation()
        self.current_correlation = correlation
        self.correlation_history.append(correlation)
        
        # Calculate decision similarity
        similarity = self._calculate_decision_similarity()
        self.current_similarity = similarity
        self.similarity_history.append(similarity)
        
        # Calculate overall independence score
        self.independence_score = 1.0 - max(correlation, similarity)
        
        # Check for independence alerts
        self._check_independence_alerts()
    
    def _calculate_algorithm_correlation(self) -> float:
        """Calculate correlation between algorithm decisions"""
        algorithm_ids = list(self.algorithm_decisions.keys())
        if len(algorithm_ids) < 2:
            return 0.0
        
        # Extract confidence scores for correlation calculation
        confidence_vectors = []
        for algo_id in algorithm_ids:
            decisions = list(self.algorithm_decisions[algo_id])
            if len(decisions) >= 2:
                confidences = [d["confidence"] for d in decisions]
                confidence_vectors.append(confidences)
        
        if len(confidence_vectors) < 2:
            return 0.0
        
        # Calculate correlation between confidence vectors
        try:
            correlation_matrix = np.corrcoef(confidence_vectors)
            # Get average correlation (excluding diagonal)
            correlations = []
            for i in range(len(correlation_matrix)):
                for j in range(i + 1, len(correlation_matrix)):
                    correlations.append(abs(correlation_matrix[i][j]))
            
            return np.mean(correlations) if correlations else 0.0
        except:
            return 0.0
    
    def _calculate_decision_similarity(self) -> float:
        """Calculate similarity between algorithm decisions"""
        algorithm_ids = list(self.algorithm_decisions.keys())
        if len(algorithm_ids) < 2:
            return 0.0
        
        # Extract actions for similarity calculation
        action_vectors = []
        for algo_id in algorithm_ids:
            decisions = list(self.algorithm_decisions[algo_id])
            if len(decisions) >= 2:
                actions = [d["action"] for d in decisions]
                action_vectors.append(actions)
        
        if len(action_vectors) < 2:
            return 0.0
        
        # Calculate action similarity
        similarities = []
        for i in range(len(action_vectors)):
            for j in range(i + 1, len(action_vectors)):
                vec1, vec2 = action_vectors[i], action_vectors[j]
                min_len = min(len(vec1), len(vec2))
                if min_len > 0:
                    matches = sum(1 for k in range(min_len) if vec1[k] == vec2[k])
                    similarity = matches / min_len
                    similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _check_independence_alerts(self):
        """Check for independence alerts"""
        alerts = []
        
        # Check correlation threshold
        if self.current_correlation > self.correlation_threshold:
            alerts.append({
                "type": "HIGH_CORRELATION",
                "value": self.current_correlation,
                "threshold": self.correlation_threshold,
                "severity": "WARNING" if self.current_correlation < 0.8 else "CRITICAL"
            })
        
        # Check similarity threshold
        if self.current_similarity > self.similarity_threshold:
            alerts.append({
                "type": "HIGH_SIMILARITY",
                "value": self.current_similarity,
                "threshold": self.similarity_threshold,
                "severity": "WARNING" if self.current_similarity < 0.9 else "CRITICAL"
            })
        
        # Store alerts
        if alerts:
            self.independence_alerts.extend(alerts)
            for alert in alerts:
                logger.warning(f"🛡️ Independence Alert: {alert['type']} = {alert['value']:.3f} (threshold: {alert['threshold']})", operation="enhanced_logging")
    
    def get_independence_status(self) -> Dict[str, Any]:
        """Get current independence status"""
        return {
            "independence_score": self.independence_score,
            "correlation": self.current_correlation,
            "similarity": self.current_similarity,
            "status": self._get_independence_status(),
            "alerts": self.independence_alerts[-10:],  # Last 10 alerts
            "monitoring_active": True
        }
    
    def _get_independence_status(self) -> str:
        """Get independence status string"""
        if self.independence_score > 0.7:
            return "EXCELLENT"
        elif self.independence_score > 0.5:
            return "GOOD"
        elif self.independence_score > 0.3:
            return "FAIR"
        else:
            return "POOR"


class SafeKnowledgeSharing:
    """
    🚀 MINIMAL, SAFE KNOWLEDGE SHARING SYSTEM
    =========================================
    Shares only non-decision-influencing information
    Preserves algorithm independence while improving safety
    """
    
    def __init__(self, enable_independence_monitoring: bool = True):
        """
        Initialize safe knowledge sharing system
        
        Args:
            enable_independence_monitoring: Enable independence monitoring safeguard
        """
        self.enable_independence_monitoring = enable_independence_monitoring
        
        # Initialize independence monitor if enabled
        if enable_independence_monitoring:
            self.independence_monitor = IndependenceMonitor()
        else:
            self.independence_monitor = None
        
        # Knowledge sharing state
        self.shared_risk_warnings = deque(maxlen=1000)
        self.shared_regime_info = deque(maxlen=1000)
        self.shared_quality_alerts = deque(maxlen=1000)
        
        # Sharing statistics
        self.sharing_stats = {
            "risk_warnings_shared": 0,
            "regime_info_shared": 0,
            "quality_alerts_shared": 0,
            "sharing_blocked": 0
        }
        
        logger.info("🚀 Safe Knowledge Sharing System initialized", operation="enhanced_logging")
        logger.info(f"   🛡️ Independence monitoring: {'ENABLED' if enable_independence_monitoring else 'DISABLED'}", operation="enhanced_logging")
    
    def share_risk_warning(self, risk_warning: RiskWarning) -> bool:
        """
        Share risk warning (SAFE - no decision influence)
        
        Args:
            risk_warning: Risk warning to share
            
        Returns:
            bool: True if shared successfully, False if blocked
        """
        # Validate risk warning
        if not self._validate_risk_warning(risk_warning):
            logger.warning(f"⚠️ Risk warning validation failed: {risk_warning.symbol}", operation="enhanced_logging")
            self.sharing_stats["sharing_blocked"] += 1
            return False
        
        # Check independence before sharing
        if self.independence_monitor:
            independence_status = self.independence_monitor.get_independence_status()
            if independence_status["status"] == "POOR":
                logger.warning("🛡️ Risk warning sharing blocked due to poor independence", operation="enhanced_logging")
                self.sharing_stats["sharing_blocked"] += 1
                return False
        
        # Share risk warning
        self.shared_risk_warnings.append(risk_warning)
        self.sharing_stats["risk_warnings_shared"] += 1
        
        logger.info(f"🚨 Risk warning shared: {risk_warning.symbol} - {risk_warning.risk_type} ({risk_warning.risk_level.value})", operation="enhanced_logging")
        return True
    
    def share_market_regime(self, regime_info: MarketRegimeInfo) -> bool:
        """
        Share market regime information (SAFE - no decision influence)
        
        Args:
            regime_info: Market regime information to share
            
        Returns:
            bool: True if shared successfully, False if blocked
        """
        # Validate regime info
        if not self._validate_regime_info(regime_info):
            logger.warning(f"⚠️ Market regime validation failed: {regime_info.symbol}", operation="enhanced_logging")
            self.sharing_stats["sharing_blocked"] += 1
            return False
        
        # Check independence before sharing
        if self.independence_monitor:
            independence_status = self.independence_monitor.get_independence_status()
            if independence_status["status"] == "POOR":
                logger.warning("🛡️ Market regime sharing blocked due to poor independence", operation="enhanced_logging")
                self.sharing_stats["sharing_blocked"] += 1
                return False
        
        # Share regime info
        self.shared_regime_info.append(regime_info)
        self.sharing_stats["regime_info_shared"] += 1
        
        logger.info(f"📊 Market regime shared: {regime_info.symbol} - {regime_info.regime.value} (confidence: {regime_info.confidence:.3f})", operation="enhanced_logging")
        return True
    
    def share_data_quality_alert(self, quality_alert: DataQualityAlert) -> bool:
        """
        Share data quality alert (SAFE - operational only)
        
        Args:
            quality_alert: Data quality alert to share
            
        Returns:
            bool: True if shared successfully, False if blocked
        """
        # Validate quality alert
        if not self._validate_quality_alert(quality_alert):
            logger.warning(f"⚠️ Data quality alert validation failed: {quality_alert.symbol}", operation="enhanced_logging")
            self.sharing_stats["sharing_blocked"] += 1
            return False
        
        # Data quality alerts are always safe to share (operational only)
        self.shared_quality_alerts.append(quality_alert)
        self.sharing_stats["quality_alerts_shared"] += 1
        
        logger.info(f"🔧 Data quality alert shared: {quality_alert.symbol} - {quality_alert.alert_type} ({quality_alert.severity})", operation="enhanced_logging")
        return True
    
    def record_algorithm_decision(self, algorithm_id: str, decision: Dict[str, Any]):
        """Record algorithm decision for independence monitoring"""
        if self.independence_monitor:
            self.independence_monitor.record_algorithm_decision(algorithm_id, decision)
    
    def _validate_risk_warning(self, risk_warning: RiskWarning) -> bool:
        """Validate risk warning before sharing"""
        if not risk_warning.symbol or not risk_warning.risk_type:
            return False
        
        if risk_warning.confidence < 0.0 or risk_warning.confidence > 1.0:
            return False
        
        if risk_warning.timestamp > datetime.now():
            return False
        
        return True
    
    def _validate_regime_info(self, regime_info: MarketRegimeInfo) -> bool:
        """Validate market regime info before sharing"""
        if not regime_info.symbol or not regime_info.regime:
            return False
        
        if regime_info.confidence < 0.0 or regime_info.confidence > 1.0:
            return False
        
        if regime_info.timestamp > datetime.now():
            return False
        
        return True
    
    def _validate_quality_alert(self, quality_alert: DataQualityAlert) -> bool:
        """Validate data quality alert before sharing"""
        if not quality_alert.symbol or not quality_alert.alert_type:
            return False
        
        if quality_alert.timestamp > datetime.now():
            return False
        
        return True
    
    def get_sharing_status(self) -> Dict[str, Any]:
        """Get current sharing status and statistics"""
        status = {
            "sharing_active": True,
            "independence_monitoring": self.enable_independence_monitoring,
            "statistics": self.sharing_stats.copy(),
            "recent_risk_warnings": len(self.shared_risk_warnings),
            "recent_regime_info": len(self.shared_regime_info),
            "recent_quality_alerts": len(self.shared_quality_alerts)
        }
        
        # Add independence status if monitoring is enabled
        if self.independence_monitor:
            status["independence_status"] = self.independence_monitor.get_independence_status()
        
        return status
    
    def get_shared_risk_warnings(self, symbol: Optional[str] = None, 
                                risk_level: Optional[RiskLevel] = None,
                                hours_back: int = 24) -> List[RiskWarning]:
        """Get shared risk warnings with optional filtering"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        filtered_warnings = []
        for warning in self.shared_risk_warnings:
            if warning.timestamp < cutoff_time:
                continue
            
            if symbol and warning.symbol != symbol:
                continue
            
            if risk_level and warning.risk_level != risk_level:
                continue
            
            filtered_warnings.append(warning)
        
        return filtered_warnings
    
    def get_shared_regime_info(self, symbol: Optional[str] = None,
                              hours_back: int = 24) -> List[MarketRegimeInfo]:
        """Get shared market regime information with optional filtering"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        filtered_regime = []
        for regime in self.shared_regime_info:
            if regime.timestamp < cutoff_time:
                continue
            
            if symbol and regime.symbol != symbol:
                continue
            
            filtered_regime.append(regime)
        
        return filtered_regime
    
    def get_shared_quality_alerts(self, symbol: Optional[str] = None,
                                 hours_back: int = 24) -> List[DataQualityAlert]:
        """Get shared data quality alerts with optional filtering"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        filtered_alerts = []
        for alert in self.shared_quality_alerts:
            if alert.timestamp < cutoff_time:
                continue
            
            if symbol and alert.symbol != symbol:
                continue
            
            filtered_alerts.append(alert)
        
        return filtered_alerts


# Factory function for easy initialization
def create_safe_knowledge_sharing(enable_independence_monitoring: bool = True) -> SafeKnowledgeSharing:
    """
    Create and initialize safe knowledge sharing system
    
    Args:
        enable_independence_monitoring: Enable independence monitoring safeguard
        
    Returns:
        SafeKnowledgeSharing: Initialized safe knowledge sharing system
    """
    return SafeKnowledgeSharing(enable_independence_monitoring=enable_independence_monitoring)
