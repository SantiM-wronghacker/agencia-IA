import React, { useState, useEffect, useCallback } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

interface WsEvent {
  type: string;
  timestamp: string;
  data?: unknown;
}

const RealtimeUpdates: React.FC = () => {
  const { lastMessage, isConnected } = useWebSocket();
  const [events, setEvents] = useState<WsEvent[]>([]);

  const processMessage = useCallback((msg: unknown) => {
    let event: WsEvent;
    if (typeof msg === 'object' && msg !== null) {
      const obj = msg as Record<string, unknown>;
      // Backend sends 'event' field, map to 'type' for display
      const eventType = (obj.event as string) || (obj.type as string) || 'message';
      event = {
        type: eventType,
        timestamp: (obj.timestamp as string) || new Date().toISOString(),
        data: obj.task || obj.data || obj,
      };
    } else {
      event = { type: 'message', timestamp: new Date().toISOString(), data: msg };
    }

    setEvents((prev) => [event, ...prev].slice(0, 10));
  }, []);

  useEffect(() => {
    if (lastMessage) {
      processMessage(lastMessage);
    }
  }, [lastMessage, processMessage]);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-medium">Realtime Updates</h3>
        <div className="flex items-center space-x-2 text-sm">
          <span
            className={`h-2.5 w-2.5 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span className="text-gray-500 dark:text-gray-400">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {events.length === 0 ? (
        <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-4">
          No events yet. Waiting for updates...
        </p>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {events.map((event, idx) => (
            <div
              key={`${event.timestamp}-${idx}`}
              className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-700/50 rounded px-3 py-2"
            >
              <span className="font-mono text-indigo-600 dark:text-indigo-400">
                {event.type}
              </span>
              <span className="text-xs text-gray-400">
                {new Date(event.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RealtimeUpdates;
