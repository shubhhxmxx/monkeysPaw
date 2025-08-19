import { Component, EventEmitter, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { WishService } from '../services/wish.service';

@Component({
  selector: 'app-wish-input',
  standalone: true,
  templateUrl: './wish-input.html',
  styleUrls: ['./wish-input.scss'],
  imports: [FormsModule]
})
export class WishInputComponent {
  @Output() wishSubmitted = new EventEmitter<string>();
  @Output() curseReceived = new EventEmitter<string>();

  wish = '';
  error = '';
  loading = false;
  private api = inject(WishService);

  submitWish() {
    const current = this.wish.trim();
    if (!current || this.loading) return;
    this.wishSubmitted.emit(current);
    this.loading = true;
    console.log(current);
    this.api.createWish(current).subscribe({
      next: (response) => {
        this.loading = false;
        this.wish = ''; // Clear input
        console.log('Wish created:', response);
        this.curseReceived.emit(response.twist); // Emit the twisted curse
      },
      error: (err) => {
        this.loading = false;
        console.error('Error creating wish:', err);
        this.error = 'Failed to create wish. Please try again.';
      }
    });
  }
}