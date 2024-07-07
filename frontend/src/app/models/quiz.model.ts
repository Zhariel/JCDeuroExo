export interface Model {
  value: string;
  viewValue: string;
}

export interface Option {
  text: string;
  isCorrect: boolean;
}

export interface Question {
  question: string;
  options: Option[];
  context: string;
}
