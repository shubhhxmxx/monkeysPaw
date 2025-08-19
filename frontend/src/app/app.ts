import { Component } from '@angular/core';
import { ChatComponent } from './chat-component/chat-component';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
  standalone: true,
  imports: [ChatComponent]
})
export class AppComponent { }