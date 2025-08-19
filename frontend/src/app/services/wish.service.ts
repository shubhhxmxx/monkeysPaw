import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../environments/environment';

export interface WishRequest {
  wish: string;
}
export interface WishResponse {
  id: BigInteger;
  wish: string;
  twist: string;
}

@Injectable({ providedIn: 'root' })
export class WishService {
  private http = inject(HttpClient);
  private base = environment.apiBase;

  createWish(raw: string) {
    const wish = raw.trim();
    if (!wish) throw new Error('Empty wish');
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body: WishRequest = { wish }; // or { text: wish } if backend expects 'text'
    console.log('Creating wish:', body);
    console.log('API Base URL:', this.base);
    console.log('[WishService] POST', `${this.base}/wishes`, body);

    return this.http.post<WishResponse>(`${this.base}/wishes`,  body , { headers });
  }

  reset(){
    console.log('Resetting wishes');
    return this.http.post(`${this.base}/wishes/reset`, {});
  }
}