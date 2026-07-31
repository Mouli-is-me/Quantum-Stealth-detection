/**
 * Single HTTP and WebSocket client for the Tactical Command & Control frontend.
 * Only place where network calls occur.
 */

export class ApiClient {
  private static baseUrl = '';

  public static async fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data as T;
    } catch (error: any) {
      console.error(`[API CLIENT ERROR] Failed request to ${endpoint}:`, error);
      throw error;
    }
  }

  public static createWebSocket(path: string, onMessage: (msg: any) => void, onError: (err: any) => void): WebSocket {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}${path}`;
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (err) {
        onError(err);
      }
    };

    ws.onerror = (err) => {
      onError(err);
    };

    return ws;
  }
}
