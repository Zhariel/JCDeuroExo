import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInput } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
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
    MatCheckboxModule,
    FormsModule
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})

export class HomeComponent implements OnInit {
  availableEuroYears: number[] = [];
  availableModels: Model[] = [];
  euroYear: number = 2020;
  enableRAG: boolean = true;
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
    this.enableRAG = this.quizDataService.getEnableRAG();
  } 

  validateEuroYear() {
    if (!this.availableEuroYears.includes(this.euroYear)) {
      alert(`Invalid year! Please select one of the following: ${this.availableEuroYears.join(', ')}`);
      this.euroYear = 2020;
    }
  }

  onEnableRAGChange() {
    this.quizDataService.setEnableRAG(this.enableRAG);
  }  

  startQuiz() {
    const selectedModel = this.availableModels.find(
      (model) => model.value === this.modelValue
    );
    if (selectedModel) {
      this.quizDataService.setEuroYear(this.euroYear);
      this.quizDataService.setModel(selectedModel);
      this.quizDataService.setEnableRAG(this.enableRAG);

      const queryParams = new URLSearchParams({
        model: selectedModel.value,
        euroYear: this.euroYear.toString(),
        enableRAG: this.enableRAG.toString(),
      });

      this.router.navigate(['/quiz'], { queryParams: queryParams });
    } else {
      console.error('Selected model not found');
    }
  }
}
