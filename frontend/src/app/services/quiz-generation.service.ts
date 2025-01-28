import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Question } from '../models/quiz.model';

@Injectable({
  providedIn: 'root',
})
export class QuizGenerationService {
  private apiUrl = 'http://localhost:8000/';

  constructor(private http: HttpClient) {}

  generateQuiz(euroYear: number, model: string, enableRAG: boolean): Observable<Question[]> {
    return this.http.get<Question[]>(
      `${this.apiUrl}?model=${model}&euroYear=${euroYear}&enableRAG=${enableRAG}`
    );
  }
}
