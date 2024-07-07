import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Model } from '../models/quiz.model';
import { QuizDataService } from '../services/quiz-data.service';

@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule],
  templateUrl: './result.component.html',
  styleUrl: './result.component.scss',
})
export class ResultComponent implements OnInit {
  euroYear: number = 2020;
  model: Model = { value: 'mistral', viewValue: 'Mistral 7B' };
  score: number = 0;
  total: number = 0;

  constructor(
    private quizDataService: QuizDataService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.quizDataService.currentEuroYear.subscribe((currentEuroYear) => {
      this.euroYear = currentEuroYear;
    });
    this.quizDataService.currentModel.subscribe((currentModel) => {
      this.model = currentModel;
    });
    this.quizDataService.currentScore.subscribe((currentScore) => {
      this.score = currentScore;
    });
    this.quizDataService.currentTotal.subscribe((currentTotal) => {
      this.total = currentTotal;
    });
  }

  goBackHome(): void {
    this.router.navigate(['/']);
  }
}
