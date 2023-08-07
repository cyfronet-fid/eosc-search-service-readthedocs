import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchInputComponent } from './search-input.component';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { NzTagModule } from 'ng-zorro-antd/tag';

@NgModule({
  declarations: [SearchInputComponent],
  imports: [CommonModule, RouterModule, ReactiveFormsModule, NzTagModule],
  exports: [SearchInputComponent],
})
export class SearchInputModule {}
