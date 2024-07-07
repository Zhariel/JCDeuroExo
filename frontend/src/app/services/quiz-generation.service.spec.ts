import { TestBed } from '@angular/core/testing';

import { QuizGenerationService } from './quiz-generation.service';

describe('QuizGenerationService', () => {
  let service: QuizGenerationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(QuizGenerationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
