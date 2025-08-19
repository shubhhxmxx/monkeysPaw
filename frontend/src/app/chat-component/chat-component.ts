import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MessageBubbleComponent } from '../message-bubble/message-bubble';
import { WishInputComponent } from '../wish-input/wish-input';
import { ChatService } from '../chat-component/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  templateUrl: './chat-component.html',
  styleUrls: ['./chat-component.scss'],
  imports: [CommonModule, MessageBubbleComponent, WishInputComponent]
})
export class ChatComponent implements OnInit {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  messages: { text: string; sender: 'player' | 'paw' }[] = [];
  wishesRemaining = 3; // Limit to 3 wishes
  gameOver = false; // Track if the game is over

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    this.initializeGame();
  }

  initializeGame() {
    this.messages = [
      { text: 'Welcome to The Monkey’s Paw!', sender: 'paw' },
      { text: 'What is your first wish?', sender: 'paw' }
    ];
    this.wishesRemaining = 3;
    this.gameOver = false;
    this.scrollToBottom();
  }


  resetGame() {
    this.initializeGame(); // Reset the game state
  }
  handleCurse(curse: string) { 
    console.log("reached handleCurse:"+curse);
    this.messages.push({ text: curse, sender: 'paw' });
    this.wishesRemaining--;
    if (this.wishesRemaining === 0) {
      this.messages.push({ text: 'You have used all your wishes. Reset the game to continue.', sender: 'paw' });
      this.gameOver = true;
    }
    this.scrollToBottom();
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop =
          this.messagesContainer.nativeElement.scrollHeight;
      }
    }, 0);
  }
}