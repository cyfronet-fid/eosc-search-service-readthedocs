import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { FilterMultiselectService } from './filter-multiselect.service';
import { FilterTreeNode } from '../types';
import { FilterMultiselectRepository } from './filter-multiselect.repository';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';
import { debounceTime, map, skip, switchMap, tap } from 'rxjs';
import { UntypedFormControl } from '@angular/forms';
import { CustomRoute } from '@collections/services/custom-route.service';
import { combineLatest } from 'rxjs';
import { Router } from '@angular/router';
import { toArray } from '@collections/filters-serializers/utils';
import { FiltersConfigsRepository } from '@collections/repositories/filters-configs.repository';
import {
  deserializeAll,
  removeFilterValue,
} from '@collections/filters-serializers/filters-serializers.utils';

@UntilDestroy()
@Component({
  selector: 'ess-filter-multiselect',
  template: `
    <div class="filter" *ngIf="hasEntities$ | async">
      <span class="filter-title"
        ><b>{{ label }}</b></span
      >
      <span (click)="resetAllActiveEntities()">
        &nbsp; &nbsp;
        <a href="javascript:void(0)" class="clear-button">clear all</a>
      </span>

      <ng-container *ngIf="(isLoading$ | async) === false">
        <ess-checkboxes-tree
          [data]="$any(activeEntities$ | async)"
          (checkboxesChange)="$event[1] === false ? toggleActive($event) : null"
        ></ess-checkboxes-tree>
        <ess-checkboxes-tree
          *ngIf="!showMore"
          [data]="$any(limitedNonActiveEntities$ | async)"
          (checkboxesChange)="$event[1] === true ? toggleActive($event) : null"
        ></ess-checkboxes-tree>

        <ng-container *ngIf="showMore">
          <input
            [attr.placeholder]="'Search...'"
            class="query-input form-control form-control-sm"
            [formControl]="queryFc"
          />
          <div class="filter__viewport" (scroll)="onScroll($event)" #content>
            <ess-checkboxes-tree
              [data]="$any(chunkedEntities$ | async)"
              (checkboxesChange)="
                $event[1] === true ? toggleActive($event) : null
              "
            ></ess-checkboxes-tree>
          </div>
        </ng-container>
        <span *ngIf="hasShowMore$ | async" (click)="showMore = !showMore">
          <a href="javascript:void(0)" class="show-more">{{
            showMore ? 'show less' : 'show more'
          }}</a>
        </span>
      </ng-container>

      <ng-container *ngIf="isLoading$ | async">
        <nz-skeleton-element
          nzType="input"
          [nzActive]="true"
          nzSize="small"
          style="width: 100%; padding-bottom: 5px"
        ></nz-skeleton-element>
        <nz-skeleton-element
          nzType="input"
          [nzActive]="true"
          nzSize="small"
          style="width: 100%; padding-bottom: 5px"
        ></nz-skeleton-element>
        <nz-skeleton-element
          nzType="input"
          [nzActive]="true"
          nzSize="small"
          style="width: 100%; padding-bottom: 5px"
        ></nz-skeleton-element>
      </ng-container>
    </div>
  `,
  styles: [
    `
      .filter__viewport {
        max-height: 290px;
        overflow: auto;
      }
      .filter {
        margin-bottom: 10px;
      }
      .filter-title {
        padding-bottom: 6px;
        display: inline-block;
      }
      .query-input {
        margin-bottom: 12px;
      }
    `,
  ],
  providers: [FilterMultiselectService, FilterMultiselectRepository],
})
export class FilterMultiselectComponent implements OnInit {
  @ViewChild('content', { static: false }) content?: unknown;

  @Input()
  label!: string;

  @Input()
  set filter(filter: string) {
    this._filter = filter;
    this._filterMultiselectService.filter = filter;
  }

  _filter = '';
  showMore = false;
  hasShowMore$ = this._filterMultiselectService.hasShowMore$;

  isLoading$ = this._filterMultiselectService.isLoading$;
  activeEntities$ = this._filterMultiselectService.activeEntities$;

  chunkedEntities$ = this._filterMultiselectService.chunkedNonActiveEntities$;
  limitedNonActiveEntities$ =
    this._filterMultiselectService.limitedNonActiveEntities$;

  hasEntities$ = this._filterMultiselectService.hasEntities$;

  queryFc = new UntypedFormControl('');

  onScroll = this._filterMultiselectService.onScroll;

  constructor(
    private _customRoute: CustomRoute,
    private _router: Router,
    private _filtersConfigsRepository: FiltersConfigsRepository,
    private _filterMultiselectService: FilterMultiselectService
  ) {}

  ngOnInit() {
    this._filterMultiselectService
      ._loadAllAvailableValues$(
        this._customRoute.params()['collection'] as string
      )
      .pipe(
        untilDestroyed(this),
        tap(() =>
          this._filterMultiselectService.setActiveIds(
            toArray(
              this._customRoute.fqMap()[this._filterMultiselectService.filter]
            )
          )
        ),
        switchMap(() =>
          this._filterMultiselectService
            ._updateCounts$({
              ...this._customRoute.params(),
              fq: this._customRoute.fqWithExcludedFilter(
                this._filterMultiselectService.filter
              ),
            })
            .pipe(untilDestroyed(this))
        )
      )
      .subscribe();

    this._customRoute.fqMap$
      .pipe(
        untilDestroyed(this),
        skip(1),
        map((fqMap) => fqMap[this._filter] ?? []),
        tap((activeIds) =>
          this._filterMultiselectService.setActiveIds(toArray(activeIds))
        )
      )
      .subscribe();

    // load on changes other than collection
    combineLatest(
      this._customRoute
        .fqWithExcludedFilter$(this._filter)
        .pipe(untilDestroyed(this)),
      this._customRoute.q$.pipe(untilDestroyed(this))
    )
      .pipe(
        skip(1),
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        map(([fq, _]) => fq),
        switchMap((fq) =>
          this._filterMultiselectService._updateCounts$({
            ...this._customRoute.params(),
            fq,
          })
        )
      )
      .subscribe();

    this._filterMultiselectService.initNonActiveEntitiesChunk$
      .pipe(untilDestroyed(this))
      .subscribe();

    this.queryFc.valueChanges
      .pipe(untilDestroyed(this), debounceTime(300))
      .subscribe((query) => this._filterMultiselectService.setQuery(query));
  }

  async resetAllActiveEntities() {
    await this._router.navigate([], {
      queryParams: {
        fq: this._customRoute
          .fq()
          .filter(
            (fq) => !fq.startsWith(this._filterMultiselectService.filter)
          ),
      },
      queryParamsHandling: 'merge',
    });
  }

  async toggleActive(event: [FilterTreeNode, boolean]) {
    const [node, currentIsSelected] = event;
    const { filter, value, isSelected } = node;
    if (isSelected === currentIsSelected) {
      return;
    }

    if (currentIsSelected) {
      await this._router.navigate([], {
        queryParams: {
          fq: this._addFilterValue(filter, value),
        },
        queryParamsHandling: 'merge',
      });
      return;
    }
    await this._router.navigate([], {
      queryParams: {
        fq: removeFilterValue(
          this._customRoute.fqMap(),
          filter,
          value,
          this._filtersConfigsRepository.get(this._customRoute.collection())
            .filters
        ),
      },
      queryParamsHandling: 'merge',
    });
  }

  _addFilterValue(filterName: string, value: string): string[] {
    const fqMap = this._customRoute.fqMap();
    const filtersConfigs = this._filtersConfigsRepository.get(
      this._customRoute.collection()
    ).filters;
    if (
      !!fqMap[filterName] &&
      (fqMap[filterName] as string[]).includes(value)
    ) {
      return deserializeAll(fqMap, filtersConfigs);
    }

    fqMap[filterName] = fqMap[filterName]
      ? ([...fqMap[filterName], value] as string[])
      : [value];
    return deserializeAll(fqMap, filtersConfigs);
  }
}