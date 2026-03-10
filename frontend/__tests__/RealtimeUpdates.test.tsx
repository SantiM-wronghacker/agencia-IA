import React from 'react';
import { render, screen, act } from '@testing-library/react';

// --- mock the useWebSocket hook ------------------------------------------
let mockLastMessage: unknown = null;
let mockIsConnected = false;
const setLastMessage = (msg: unknown) => { mockLastMessage = msg; };
const setIsConnected = (val: boolean) => { mockIsConnected = val; };

jest.mock('../src/hooks/useWebSocket', () => ({
  useWebSocket: () => ({
    lastMessage: mockLastMessage,
    isConnected: mockIsConnected,
  }),
}));

import RealtimeUpdates from '../src/components/RealtimeUpdates';

beforeEach(() => {
  mockLastMessage = null;
  mockIsConnected = false;
});

test('shows Disconnected when WS is not connected', () => {
  render(<RealtimeUpdates />);
  expect(screen.getByText('Disconnected')).toBeTruthy();
});

test('shows Connected when WS is connected', () => {
  setIsConnected(true);
  render(<RealtimeUpdates />);
  expect(screen.getByText('Connected')).toBeTruthy();
});

test('shows waiting message when no events', () => {
  render(<RealtimeUpdates />);
  expect(screen.getByText(/No events yet/)).toBeTruthy();
});

test('renders event from unified envelope { event, ts, payload }', () => {
  setLastMessage({
    event: 'task_created',
    ts: '2025-01-01T00:00:00Z',
    payload: { id: '1', name: 'Test' },
  });
  render(<RealtimeUpdates />);
  expect(screen.getByText('task_created')).toBeTruthy();
});

test('renders event from legacy { type } format', () => {
  setLastMessage({
    type: 'legacy_event',
    timestamp: '2025-06-01T12:00:00Z',
  });
  render(<RealtimeUpdates />);
  expect(screen.getByText('legacy_event')).toBeTruthy();
});

test('falls back to "message" type for unknown shapes', () => {
  setLastMessage('plain string');
  render(<RealtimeUpdates />);
  expect(screen.getByText('message')).toBeTruthy();
});
