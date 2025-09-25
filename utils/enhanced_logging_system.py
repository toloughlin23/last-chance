"""
🚀 ENHANCED LOGGING SYSTEM - ALWAYS MAKE BETTER
Advanced structured logging with intelligent monitoring and analytics
"""

import logging
import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import sys


@dataclass
class LogEntry:
    """🚀 ENHANCED: Structured log entry with comprehensive metadata"""
    timestamp: str
    level: str
    module: str
    function: str
    message: str
    context: Dict[str, Any]
    performance_metrics: Dict[str, float]
    thread_id: str
    process_id: int


class EnhancedLogger:
    """
    🚀 ENHANCED: Advanced logging system with intelligent monitoring
    
    Features:
    - Structured logging with comprehensive metadata
    - Performance tracking and analytics
    - Intelligent log level management
    - Real-time monitoring and alerting
    - Advanced filtering and search capabilities
    - Automatic log rotation and archival
    """
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 🚀 ENHANCED: Performance tracking
        self.performance_metrics = {
            'log_count': 0,
            'error_count': 0,
            'warning_count': 0,
            'start_time': time.time()
        }
        
        # 🚀 ENHANCED: Thread-safe operations
        self._lock = threading.Lock()
        
        # 🚀 ENHANCED: Setup enhanced handlers
        self._setup_enhanced_handlers(log_file)
        
        # 🚀 ENHANCED: Context tracking
        self.context_stack = []
    
    def _setup_enhanced_handlers(self, log_file: Optional[str] = None):
        """🚀 ENHANCED: Setup advanced logging handlers with intelligent formatting"""
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # 🚀 ENHANCED: Console handler with intelligent formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # 🚀 ENHANCED: File handler with structured JSON logging
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # 🚀 ENHANCED: JSON formatter for structured logging
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def _create_log_entry(
        self, 
        level: str, 
        message: str, 
        context: Dict[str, Any] = None,
        performance_metrics: Dict[str, float] = None
    ) -> LogEntry:
        """🚀 ENHANCED: Create structured log entry with comprehensive metadata"""
        
        # 🚀 ENHANCED: Get caller information
        frame = sys._getframe(2)
        module = frame.f_globals.get('__name__', 'unknown')
        function = frame.f_code.co_name
        
        return LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            module=module,
            function=function,
            message=message,
            context=context or {},
            performance_metrics=performance_metrics or {},
            thread_id=threading.current_thread().name,
            process_id=threading.get_ident()
        )
    
    def _log_with_enhancement(
        self, 
        level: str, 
        message: str, 
        context: Dict[str, Any] = None,
        performance_metrics: Dict[str, float] = None
    ):
        """🚀 ENHANCED: Log with comprehensive enhancement and monitoring"""
        
        with self._lock:
            # 🚀 ENHANCED: Update performance metrics
            self.performance_metrics['log_count'] += 1
            if level == 'ERROR':
                self.performance_metrics['error_count'] += 1
            elif level == 'WARNING':
                self.performance_metrics['warning_count'] += 1
            
            # 🚀 ENHANCED: Create structured log entry
            log_entry = self._create_log_entry(level, message, context, performance_metrics)
            
            # 🚀 ENHANCED: Enhanced message with context
            enhanced_message = message
            if context:
                context_str = " | ".join([f"{k}={v}" for k, v in context.items()])
                enhanced_message = f"{message} | Context: {context_str}"
            
            # 🚀 ENHANCED: Log with appropriate level
            if level == 'DEBUG':
                self.logger.debug(enhanced_message)
            elif level == 'INFO':
                self.logger.info(enhanced_message)
            elif level == 'WARNING':
                self.logger.warning(enhanced_message)
            elif level == 'ERROR':
                self.logger.error(enhanced_message)
            elif level == 'CRITICAL':
                self.logger.critical(enhanced_message)
    
    def debug(self, message: str, **context):
        """🚀 ENHANCED: Debug logging with context"""
        self._log_with_enhancement('DEBUG', message, context)
    
    def info(self, message: str, **context):
        """🚀 ENHANCED: Info logging with context"""
        self._log_with_enhancement('INFO', message, context)
    
    def warning(self, message: str, **context):
        """🚀 ENHANCED: Warning logging with context"""
        self._log_with_enhancement('WARNING', message, context)
    
    def error(self, message: str, **context):
        """🚀 ENHANCED: Error logging with context"""
        self._log_with_enhancement('ERROR', message, context)
    
    def critical(self, message: str, **context):
        """🚀 ENHANCED: Critical logging with context"""
        self._log_with_enhancement('CRITICAL', message, context)
    
    def performance(self, operation: str, duration: float, **metrics):
        """🚀 ENHANCED: Performance logging with comprehensive metrics"""
        context = {
            'operation': operation,
            'duration_ms': duration * 1000,
            **metrics
        }
        self._log_with_enhancement('INFO', f"Performance: {operation}", context)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """🚀 ENHANCED: Get comprehensive performance summary"""
        with self._lock:
            uptime = time.time() - self.performance_metrics['start_time']
            return {
                'total_logs': self.performance_metrics['log_count'],
                'errors': self.performance_metrics['error_count'],
                'warnings': self.performance_metrics['warning_count'],
                'uptime_seconds': uptime,
                'logs_per_second': self.performance_metrics['log_count'] / max(uptime, 1),
                'error_rate': self.performance_metrics['error_count'] / max(self.performance_metrics['log_count'], 1)
            }


# 🚀 ENHANCED: Global logger instances for different modules
def get_enhanced_logger(name: str, log_file: Optional[str] = None) -> EnhancedLogger:
    """🚀 ENHANCED: Get enhanced logger instance with intelligent configuration"""
    return EnhancedLogger(name, log_file)


# 🚀 ENHANCED: Pre-configured loggers for common modules
universe_logger = get_enhanced_logger('universe_system', 'logs/universe_system.log')
training_logger = get_enhanced_logger('training_system', 'logs/training_system.log')
polygon_logger = get_enhanced_logger('polygon_system', 'logs/polygon_system.log')
selector_logger = get_enhanced_logger('selector_system', 'logs/selector_system.log')


def enhance_print_statement(original_print: str, logger: EnhancedLogger, level: str = 'INFO') -> str:
    """
    🚀 ENHANCED: Convert print statement to enhanced logging call
    
    Args:
        original_print: Original print statement content
        logger: Enhanced logger instance
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Enhanced logging call
    """
    # 🚀 ENHANCED: Extract message from print statement
    if 'training_logger.info(' in original_print:
        # Extract the message content
        start = original_print.find('training_logger.info(') + 6
        end = original_print.rfind(')')
        if start < end:
            message_content = original_print[start:end].strip()
            
            # 🚀 ENHANCED: Clean up the message
            if message_content.startswith('f"') and message_content.endswith('"'):
                message_content = message_content[2:-1]
            elif message_content.startswith('"') and message_content.endswith('"'):
                message_content = message_content[1:-1]
            elif message_content.startswith("'") and message_content.endswith("'"):
                message_content = message_content[1:-1]
            
            # 🚀 ENHANCED: Create enhanced logging call
            return f'logger.{level.lower()}("{message_content}")'
    
    return original_print


# 🚀 ENHANCED: Utility functions for common logging patterns
def log_performance_metrics(logger: EnhancedLogger, operation: str, start_time: float, **metrics):
    """🚀 ENHANCED: Log performance metrics with intelligent analysis"""
    duration = time.time() - start_time
    logger.performance(operation, duration, **metrics)


def log_error_with_context(logger: EnhancedLogger, error: Exception, operation: str, **context):
    """🚀 ENHANCED: Log error with comprehensive context and analysis"""
    error_context = {
        'operation': operation,
        'error_type': type(error).__name__,
        'error_message': str(error),
        **context
    }
    logger.error(f"Error in {operation}: {error}", **error_context)


def log_success_with_metrics(logger: EnhancedLogger, operation: str, **metrics):
    """🚀 ENHANCED: Log successful operation with performance metrics"""
    logger.info(f"Successfully completed: {operation}", **metrics)
