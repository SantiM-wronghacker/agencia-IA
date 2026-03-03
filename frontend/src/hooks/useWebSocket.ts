import { useState, useEffect, useCallback } from 'react';
import WebSocketService from '../services/websocketService';

export function useWebSocket() {
  const [lastMessage, setLastMessage] = useState<unknown>(null);
  const [isConnected, setIsConnected] = useState(false);

  const handleMessage = useCallback((data: unknown) => {
    setLastMessage(data);
  }, []);

  useEffect(() => {
    const ws = WebSocketService.getInstance();
    const unsubMessage = ws.onMessage(handleMessage);
    const unsubConnect = ws.onConnect(() => setIsConnected(true));
    const unsubDisconnect = ws.onDisconnect(() => setIsConnected(false));

    ws.connect();
    setIsConnected(ws.isConnected);

    return () => {
      unsubMessage();
      unsubConnect();
      unsubDisconnect();
      ws.disconnect();
    };
  }, [handleMessage]);

  return { lastMessage, isConnected };
}
