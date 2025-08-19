import { inject, Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { WishService } from '../services/wish.service';

export interface ChatMsg {
  text: string;
  sender: 'player' | 'paw';
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private messagesSubject = new BehaviorSubject<ChatMsg[]>([
    { text: 'Welcome to The Monkey’s Paw!', sender: 'paw' },
    { text: 'What is your first wish?', sender: 'paw' }
  ]);
  private api =inject(WishService);
  messages$ = this.messagesSubject.asObservable();

  addMessage(text: string, sender: 'player' | 'paw') {
    console.log("reached addMessage in chat.service.ts");
    const list = this.messagesSubject.value;
    this.messagesSubject.next([...list, { text, sender }]);
  }

  reset() {
    this.messagesSubject.next([
      { text: 'Welcome to The Monkey’s Paw!', sender: 'paw' },
      { text: 'What is your first wish?', sender: 'paw' }
    ]);
  }
}