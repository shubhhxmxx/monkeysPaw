import { NgClass } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-message-bubble',
  standalone: true,
  template: `
    <div class="message-bubble" [ngClass]="sender">
      {{ message }}
    </div>
  `,
  styleUrls: ['./message-bubble.scss'],
  imports: [NgClass]
})
export class MessageBubbleComponent {
  @Input() message!: string;
  @Input() sender!: 'player' | 'paw';
}