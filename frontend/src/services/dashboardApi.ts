import api from './api';
import { Task, TaskCreate } from '../types/task';
import { DashboardMetrics, HealthResponse } from '../types/metrics';

const BASE = '/api/v2/dashboard';

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>(`${BASE}/health`);
  return data;
}

export async function getMetrics(): Promise<DashboardMetrics> {
  const { data } = await api.get<DashboardMetrics>(`${BASE}/metrics`);
  return data;
}

export async function getTasks(params?: {
  status?: string;
  search?: string;
}): Promise<Task[]> {
  const { data } = await api.get<Task[]>(`${BASE}/tasks`, { params });
  return data;
}

export async function getTask(id: string): Promise<Task> {
  const { data } = await api.get<Task>(`${BASE}/tasks/${id}`);
  return data;
}

export async function createTask(taskData: TaskCreate): Promise<Task> {
  const { data } = await api.post<Task>(`${BASE}/tasks`, taskData);
  return data;
}

export async function cancelTask(id: string): Promise<Task> {
  const { data } = await api.post<Task>(`${BASE}/tasks/${id}/cancel`);
  return data;
}

export async function getTaskLogs(id: string): Promise<string[]> {
  const { data } = await api.get<string[]>(`${BASE}/tasks/${id}/logs`);
  return data;
}
