import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-wish-input',
  standalone: true,
  template: `
    <div class="wish-input">
      <input [(ngModel)]="wish" placeholder="Enter your wish..." />
      <button (click)="submitWish()">Submit</button>
    </div>
  `,
  styleUrls: ['./wish-input.component.scss'],
  imports: [FormsModule]
})
export class WishInputComponent {
  @Output() wishSubmitted = new EventEmitter<string>();
  wish = '';

  submitWish() {
    if (this.wish.trim()) {
      this.wishSubmitted.emit(this.wish);
      this.wish = '';
    }
  }
}