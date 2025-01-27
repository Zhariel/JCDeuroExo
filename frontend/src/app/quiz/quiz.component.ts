import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Model, Option, Question } from '../models/quiz.model';
import { QuizDataService } from '../services/quiz-data.service';
import { QuizGenerationService } from '../services/quiz-generation.service';
import { combineLatest } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-quiz',
  standalone: true,
  imports: [
    CommonModule,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './quiz.component.html',
  styleUrl: './quiz.component.scss',
})
export class QuizComponent implements OnInit {
  euroYear: number = 2020;
  enableRAG: boolean = true
  model: Model = { value: 'mistral', viewValue: 'Mistral 7B' };
  questions: Question[] = [];
  currentQuestionIndex: number = 0;
  currentQuestion: Question | undefined;
  selectedOption: Option | undefined;
  answered: boolean = false;
  score: number = 0;

  constructor(
    private quizDataService: QuizDataService,
    private quizGenerationService: QuizGenerationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadQuizData();
  }

  private loadQuizData(): void {
    // Use combineLatest to ensure that the quiz is generated only after both the euro year and model are loaded
    combineLatest([
      this.quizDataService.currentEuroYear,
      this.quizDataService.currentModel,
    ]).subscribe(([euroYear, model]) => {
      this.euroYear = euroYear;
      this.model = model;
      this.generateQuiz();
    });
  }

  private generateQuiz(): void {
    this.quizGenerationService
      .generateQuiz(this.euroYear, this.model.value, this.enableRAG)
      .subscribe((questions) => {
        this.questions = questions;
        this.currentQuestion = this.questions[this.currentQuestionIndex];
      });
  }

  selectOption(option: Option): void {
    this.selectedOption = option;
    this.answered = true;
    if (option.isCorrect) {
      this.score++;
    }
  }

  nextQuestion(): void {
    this.currentQuestionIndex++;

    if (this.currentQuestionIndex < this.questions.length) {
      this.currentQuestion = this.questions[this.currentQuestionIndex];
      this.selectedOption = undefined;
      this.answered = false;
    } else {
      this.finishQuiz();
    }
  }

  private finishQuiz(): void {
    this.quizDataService.setScore(this.score);
    this.quizDataService.setTotal(this.questions.length);
    this.router.navigate(['/result']);
  }
}
