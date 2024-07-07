import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInput } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Model } from '../models/quiz.model';
import { QuizDataService } from '../services/quiz-data.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInput,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  availableEuroYears: number[] = [];
  availableModels: Model[] = [];
  euroYear: number = 2020;
  modelValue: string = 'mistral';

  constructor(
    private router: Router,
    private quizDataService: QuizDataService
  ) {}

  ngOnInit() {
    this.availableEuroYears = this.quizDataService.getAvailableEuroYears();
    this.availableModels = this.quizDataService.getAvailableModels();
    this.quizDataService.currentEuroYear.subscribe((currentEuroYear) => {
      this.euroYear = currentEuroYear;
    });
    this.quizDataService.currentModel.subscribe((currentModel) => {
      this.modelValue = currentModel.value;
    });
  }

  startQuiz() {
    const selectedModel = this.availableModels.find(
      (model) => model.value === this.modelValue
    );
    if (selectedModel) {
      this.quizDataService.setEuroYear(this.euroYear);
      this.quizDataService.setModel(selectedModel);
      this.router.navigate(['/quiz']);
    } else {
      console.error('Selected model not found');
    }
  }
}
