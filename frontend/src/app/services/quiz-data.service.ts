import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Model } from '../models/quiz.model';

@Injectable({
  providedIn: 'root',
})
export class QuizDataService {
  private availableEuroYears: number[] = [
    2024, 2020, 2016, 2012, 2008, 2004, 2000, 1996, 1992, 1988, 1984, 1980,
    1976, 1972, 1968, 1964, 1960,
  ];
  private availableModels: Model[] = [
    { value: 'mock', viewValue: 'mockQuestions.json' },
    { value: 'mistral', viewValue: 'Mistral 7B' },
    { value: 'gpt-4o', viewValue: 'OpenAI GPT-4o' },
  ];

  private euroYear = new BehaviorSubject<number>(2020);
  private model = new BehaviorSubject<Model>({
    value: 'mock',
    viewValue: 'mockQuestions.json',
  });
  private score = new BehaviorSubject<number>(0);
  private total = new BehaviorSubject<number>(5);
  private enableRAG = new BehaviorSubject<boolean>(true);

  currentEuroYear = this.euroYear.asObservable();
  currentModel = this.model.asObservable();
  currentScore = this.score.asObservable();
  currentTotal = this.total.asObservable();
  currentRAG = this.enableRAG.asObservable();

  constructor() {}

  getAvailableEuroYears(): number[] {
    return this.availableEuroYears;
  }

  getAvailableModels(): Model[] {
    return this.availableModels;
  }

  getEnableRAG(): boolean {
    return this.enableRAG.value;
  }

  setEuroYear(euroYear: number) {
    this.euroYear.next(euroYear);
  }

  setModel(model: Model) {
    this.model.next(model);
  }

  setEnableRAG(value: boolean) {
    this.enableRAG.next(value);
  }

  setScore(score: number) {
    this.score.next(score);
  }

  setTotal(total: number) {
    this.total.next(total);
  }
}
